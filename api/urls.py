# -*- coding: utf-8 -*-

from tornado.web import url
import bi.datamerge.views as datamerge_views
import bi.datasource.views as datasource_views
import bi.worktable.views as worktable_views
import bi.column.views as column_views
import bi.dashboard.views as dashboard_views
import bi.chart_page.views as chart_page_views
import bi.chart.views as chart_views
import bi.field.views as field_views
import bi.data_filter.views as data_filter_views
import bi.chart_filter.views as chart_filter_views
import bi.daterange_filter.views as daterange_filter_views
import bi.publish.views as publish_views
import bi.views as bi_views
import api.organization.team.views as team_views
import frontend.view as frontend_views
import organization.brand.views as brand_views
import organization.company.views as company_views
import organization.permission.views as permission_views
import organization.permission_type.views as permission_type_views
import organization.region.views as region_views
import organization.region_type.views as region_type_views
import organization.role.views as role_views
import organization.user.views as user_views
import organization.views as org_views
import project.dealer_project.views as dealer_project_views
import project.link.views as link_views
import project.project.views as project_views
import project.views as pro_all_views
import survey.survey.views as survey_views
import survey.views as sur_views
import wechat.views as wechat_views
import views as views
import ticket.ticket_regulation.views as ticket_regulation_views
import ticket.ticket.views as tticket_views
import ticket.ticket_record.views as ticket_record_views
import ticket.email_template.views as temail_template_views

url_mapping = [
    url(r"/api/", views.IndexHandler, name='index'),
]
