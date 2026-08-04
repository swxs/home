# -*- coding: utf-8 -*-

from apps.notify.consts import EmailTemplateType


def render_email(template_type: EmailTemplateType, action_url: str) -> tuple[str, str, str]:
    if template_type == EmailTemplateType.EMAIL_VERIFY:
        subject = "请验证您的邮箱"
        text = f"请点击以下链接验证邮箱：{action_url}\n链接 2 小时内有效。"
        html = f"""
        <html><body>
        <p>请点击下方按钮验证您的邮箱：</p>
        <p><a href="{action_url}" style="padding:10px 20px;background:#1677ff;color:#fff;text-decoration:none;border-radius:4px;">验证邮箱</a></p>
        <p>或复制链接到浏览器：{action_url}</p>
        <p>链接 2 小时内有效。</p>
        </body></html>
        """
        return subject, html, text

    subject = "重置您的密码"
    text = f"请点击以下链接重置密码：{action_url}\n链接 30 分钟内有效。"
    html = f"""
    <html><body>
    <p>请点击下方按钮重置密码：</p>
    <p><a href="{action_url}" style="padding:10px 20px;background:#1677ff;color:#fff;text-decoration:none;border-radius:4px;">重置密码</a></p>
    <p>或复制链接到浏览器：{action_url}</p>
    <p>链接 30 分钟内有效。</p>
    </body></html>
    """
    return subject, html, text
