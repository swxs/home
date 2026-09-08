# -*- coding: utf-8 -*-

from dataclasses import dataclass
from html import escape

from home.apps.notify.consts import EmailTemplateType

# 与 openapi_auth variables.less 对齐
_COLOR_PRIMARY = "#2563eb"
_COLOR_TEXT = "#0f172a"
_COLOR_TEXT_SECONDARY = "#475569"
_COLOR_TEXT_MUTED = "#94a3b8"
_COLOR_BORDER_LIGHT = "#f1f5f9"
_COLOR_BG = "#ffffff"
_COLOR_BG_PAGE = "#f8fafc"

_FONT_FAMILY = (
    "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, "
    "'Helvetica Neue', Arial, sans-serif"
)

_BRAND_NAME = "登录中心"


@dataclass(frozen=True)
class _EmailContent:
    subject: str
    title: str
    lead: str
    button_label: str
    expiry_note: str


def _content_for(template_type: EmailTemplateType) -> _EmailContent:
    if template_type == EmailTemplateType.EMAIL_VERIFY:
        return _EmailContent(
            subject="请验证您的邮箱",
            title="验证您的邮箱",
            lead="感谢注册。请点击下方按钮完成邮箱验证，验证通过后即可登录。",
            button_label="验证邮箱",
            expiry_note="此链接 2 小时内有效。",
        )
    return _EmailContent(
        subject="重置您的密码",
        title="重置密码",
        lead="我们收到了您的密码重置请求。请点击下方按钮设置新密码。",
        button_label="重置密码",
        expiry_note="此链接 30 分钟内有效。",
    )


def _render_text(content: _EmailContent, action_url: str) -> str:
    return (
        f"{_BRAND_NAME}\n\n"
        f"{content.title}\n\n"
        f"{content.lead}\n\n"
        f"{content.button_label}：{action_url}\n\n"
        f"{content.expiry_note}\n"
        f"如非本人操作，请忽略此邮件。"
    )


def _render_html(content: _EmailContent, action_url: str) -> str:
    safe_url = escape(action_url, quote=True)
    return f"""\
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>{escape(content.subject)}</title>
</head>
<body style="margin:0;padding:0;background-color:{_COLOR_BG_PAGE};font-family:{_FONT_FAMILY};">
  <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
         style="background-color:{_COLOR_BG_PAGE};padding:40px 16px;">
    <tr>
      <td align="center">
        <table role="presentation" width="100%" cellpadding="0" cellspacing="0"
               style="max-width:560px;background-color:{_COLOR_BG};border:1px solid {_COLOR_BORDER_LIGHT};border-radius:20px;">
          <tr>
            <td style="padding:32px 32px 8px;text-align:center;">
              <p style="margin:0 0 8px;font-size:13px;font-weight:600;letter-spacing:0.04em;color:{_COLOR_TEXT_MUTED};text-transform:uppercase;">
                {_BRAND_NAME}
              </p>
              <h1 style="margin:0;font-size:24px;font-weight:600;line-height:1.3;color:{_COLOR_TEXT};letter-spacing:-0.02em;">
                {escape(content.title)}
              </h1>
            </td>
          </tr>
          <tr>
            <td style="padding:8px 32px 24px;text-align:center;">
              <p style="margin:0;font-size:14px;line-height:1.6;color:{_COLOR_TEXT_SECONDARY};">
                {escape(content.lead)}
              </p>
            </td>
          </tr>
          <tr>
            <td align="center" style="padding:0 32px 24px;">
              <a href="{safe_url}"
                 style="display:inline-block;padding:12px 28px;background-color:{_COLOR_PRIMARY};color:#ffffff;font-size:14px;font-weight:600;line-height:1;text-decoration:none;border-radius:10px;">
                {escape(content.button_label)}
              </a>
            </td>
          </tr>
          <tr>
            <td style="padding:0 32px 24px;">
              <p style="margin:0 0 8px;font-size:12px;line-height:1.5;color:{_COLOR_TEXT_MUTED};">
                若按钮无法点击，请复制以下链接到浏览器：
              </p>
              <p style="margin:0;padding:12px;background-color:{_COLOR_BG_PAGE};border:1px solid {_COLOR_BORDER_LIGHT};border-radius:10px;font-size:12px;line-height:1.5;word-break:break-all;color:{_COLOR_TEXT_SECONDARY};">
                {safe_url}
              </p>
            </td>
          </tr>
          <tr>
            <td style="padding:0 32px 32px;text-align:center;">
              <p style="margin:0 0 8px;font-size:12px;line-height:1.5;color:{_COLOR_TEXT_MUTED};">
                {escape(content.expiry_note)}
              </p>
              <p style="margin:0;font-size:12px;line-height:1.5;color:{_COLOR_TEXT_MUTED};">
                如非本人操作，请忽略此邮件。
              </p>
            </td>
          </tr>
        </table>
      </td>
    </tr>
  </table>
</body>
</html>"""


def render_email(template_type: EmailTemplateType, action_url: str) -> tuple[str, str, str]:
    content = _content_for(template_type)
    return content.subject, _render_html(content, action_url), _render_text(content, action_url)
