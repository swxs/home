# -*- coding: utf-8 -*-

import unittest
from types import SimpleNamespace
from unittest.mock import AsyncMock, MagicMock

from bson import ObjectId
from fastapi import BackgroundTasks

from apps.notify.consts import EmailTemplateType
from apps.system import consts
from apps.system.services.auth_service import AuthService
from apps.system.utils.password import hash_password
from web import exceptions

USER_ID = str(ObjectId())


class _FakeBackgroundTasks(BackgroundTasks):
    def add_task(self, func, *args, **kwargs):
        return None


class AuthServiceEmailTests(unittest.IsolatedAsyncioTestCase):
    def setUp(self):
        self.db = AsyncMock()
        self.identity_repo = AsyncMock()
        self.email_service = AsyncMock()
        self.token_store = AsyncMock()
        self.service = AuthService(
            self.db,
            identity_repo=self.identity_repo,
            email_service=self.email_service,
            token_store=self.token_store,
        )
        self.bg = _FakeBackgroundTasks()

    async def test_register_creates_user_and_schedules_email(self):
        self.identity_repo.find_user_by_username.return_value = None
        self.identity_repo.find_user_auth.return_value = None
        user = SimpleNamespace(id=USER_ID)
        self.identity_repo.create_user_with_password_and_email.return_value = (user, None, None)

        result = await self.service.register("alice", "alice@example.com", "secret12", self.bg)

        self.assertEqual(result.message, "注册成功，请查收验证邮件")
        self.identity_repo.create_user_with_password_and_email.assert_awaited_once()
        self.token_store.set_token.assert_awaited_once()
        self.email_service.schedule_send.assert_awaited_once()

    async def test_register_duplicate_username(self):
        self.identity_repo.find_user_by_username.return_value = SimpleNamespace(id="x")

        with self.assertRaises(exceptions.Http409ConflictException):
            await self.service.register("alice", "alice@example.com", "secret12", self.bg)

    async def test_register_duplicate_email(self):
        self.identity_repo.find_user_by_username.return_value = None
        self.identity_repo.find_user_auth.return_value = SimpleNamespace(id="auth1")

        with self.assertRaises(exceptions.Http409ConflictException):
            await self.service.register("alice", "alice@example.com", "secret12", self.bg)

    async def test_verify_email_activates_user(self):
        self.token_store.get_and_delete_token.return_value = {"user_id": USER_ID}

        result = await self.service.verify_email("token123")

        self.assertEqual(result.message, "邮箱验证成功")
        self.identity_repo.verify_user_auths.assert_awaited_once_with(USER_ID)

    async def test_verify_email_invalid_token(self):
        self.token_store.get_and_delete_token.return_value = None

        with self.assertRaises(exceptions.Http400BadRequestException):
            await self.service.verify_email("bad")

    async def test_login_rejects_unverified_email(self):
        password_hash = hash_password("secret12")
        self.identity_repo.find_user_auth.side_effect = [
            SimpleNamespace(user_id=USER_ID, credential=password_hash),
            SimpleNamespace(ifverified=consts.UserAuth_Ifverified.UNVERIFIED),
        ]

        with self.assertRaises(exceptions.Http403ForbiddenException) as ctx:
            await self.service.refresh_token(1, "alice", "secret12")
        self.assertEqual(ctx.exception.code, exceptions.Http403ForbiddenException.EmailNotVerified)

    async def test_login_success_when_verified(self):
        password_hash = hash_password("secret12")
        self.identity_repo.find_user_auth.side_effect = [
            SimpleNamespace(user_id=USER_ID, credential=password_hash),
            SimpleNamespace(ifverified=consts.UserAuth_Ifverified.VERIFIED),
        ]

        result = await self.service.refresh_token(1, "alice", "secret12")

        self.assertIn("token", result)
        self.assertIn("refresh_token", result)

    async def test_forgot_password_unactivated_resends_verification(self):
        user = SimpleNamespace(id=USER_ID)
        email_auth = SimpleNamespace(
            user_id=USER_ID,
            identifier="alice@example.com",
            ifverified=consts.UserAuth_Ifverified.UNVERIFIED,
        )
        self.identity_repo.find_user_by_username.return_value = user
        self.identity_repo.find_user_auth.return_value = email_auth

        result = await self.service.forgot_password("alice", "alice@example.com", self.bg)

        self.assertTrue(result.unactivated)
        self.email_service.schedule_send.assert_awaited_once()

    async def test_forgot_password_activated_sends_reset(self):
        user = SimpleNamespace(id=USER_ID)
        email_auth = SimpleNamespace(
            user_id=USER_ID,
            identifier="alice@example.com",
            ifverified=consts.UserAuth_Ifverified.VERIFIED,
        )
        self.identity_repo.find_user_by_username.return_value = user
        self.identity_repo.find_user_auth.return_value = email_auth

        result = await self.service.forgot_password("alice", "alice@example.com", self.bg)

        self.assertFalse(result.unactivated)
        self.token_store.set_token.assert_awaited_once()
        self.email_service.schedule_send.assert_awaited_once()
        call_args = self.email_service.schedule_send.await_args
        self.assertEqual(call_args.args[1], EmailTemplateType.PASSWORD_RESET)

    async def test_reset_password_updates_credential(self):
        self.token_store.get_and_delete_token.return_value = {"user_id": USER_ID}

        result = await self.service.reset_password("token123", "newsecret12")

        self.assertEqual(result.message, "密码重置成功")
        self.identity_repo.update_password_credential.assert_awaited_once()

    async def test_reset_password_invalid_token(self):
        self.token_store.get_and_delete_token.return_value = None

        with self.assertRaises(exceptions.Http400BadRequestException):
            await self.service.reset_password("bad", "newsecret12")


if __name__ == "__main__":
    unittest.main()
