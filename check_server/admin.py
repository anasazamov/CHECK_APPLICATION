from django.contrib import admin
from .models import *
from .check_functions import *
from .connect_server import ssh_connect
from django_celery_beat.admin import (
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
)
from django_celery_results.models import TaskResult, GroupResult

# Register your models here.


class IsActiveFilter(admin.SimpleListFilter):
    title = "Active Status"
    parameter_name = "is_active"

    def lookups(self, request, model_admin):

        return [
            ("yes", "Active"),
            ("no", "Inactive"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "yes":

            active_ids = [obj.id for obj in queryset if is_server_alive(obj.ipv4)]
            return queryset.filter(id__in=active_ids)
        elif self.value() == "no":
            inactive_ids = [obj.id for obj in queryset if not is_server_alive(obj.ipv4)]
            return queryset.filter(id__in=inactive_ids)
        return queryset


class IsActiveFilterApp(IsActiveFilter):

    def queryset(self, request, queryset):
        if self.value() == "yes":

            active_ids = [
                obj.id for obj in queryset if is_port_open(obj.server.ipv4, obj.port)
            ]
            return queryset.filter(id__in=active_ids)
        elif self.value() == "no":
            inactive_ids = [
                obj.id
                for obj in queryset
                if not is_port_open(obj.server.ipv4, obj.port)
            ]
            return queryset.filter(id__in=inactive_ids)
        return queryset


# class IsActiveFilterDocer(IsActiveFilterApp):

#     def queryset(self, request, queryset):
#         if self.value() == "yes":

#             active_ids = [
#                 obj.id for obj in queryset if is_inner_port(obj.server.ipv4, obj.port)
#             ]
#             return queryset.filter(id__in=active_ids)
#         elif self.value() == "no":
#             inactive_ids = [
#                 obj.id
#                 for obj in queryset
#                 if not is_port_open(obj.server.ipv4, obj.port)
#             ]
#             return queryset.filter(id__in=inactive_ids)
#         return queryset


@admin.register(Server)
class ServerAdminView(admin.ModelAdmin):
    list_display = (
        "id",
        "name",
        "ipv4",
        "is_active",
        "username",
        "password",
        "company",
    )
    search_fields = ("name", "ipv4")
    list_filter = [IsActiveFilter]
    list_per_page = 100

    def is_active(self, obj: Server):
        return is_server_alive(obj.ipv4)

    def company(self, obj):
        return obj.company.name

    is_active.short_description = "Is Active"
    is_active.boolean = True


@admin.register(Application)
class ApplicationAdminView(admin.ModelAdmin):

    list_display = [
        "id",
        "name_run_on_server",
        "ipv4",
        "port",
        "server_name",
        "username",
        "password",
        "is_active",
        "company",
    ]
    search_fields = ["id", "name_run_on_server", "port"]
    list_filter = [IsActiveFilterApp]
    list_per_page = 100

    def company(self, obj):
        return obj.company.name

    def ipv4(self, obj):
        return obj.server.ipv4

    def server_name(self, obj):
        return obj.server.name

    def is_active(self, obj):
        return is_port_open(obj.server.ipv4, obj.port)

    def username(self, obj):
        return obj.server.username

    def password(self, obj):
        return obj.server.password

    is_active.short_description = "Is Active"
    is_active.boolean = True


@admin.register(DockerApplication)
class DockerApplicationAdminView(admin.ModelAdmin):

    list_display = [
        "id",
        "name_run_on_docker",
        "ipv4",
        "port",
        "server_name",
        "username",
        "password",
        "is_active",
        "company",
    ]
    search_fields = ["id", "name_run_on_docker", "port"]
    # list_filter = [IsActiveFilterApp]
    list_per_page = 100

    def company(self, obj):
        return obj.company.name

    def ipv4(self, obj):
        return obj.server.ipv4

    def server_name(self, obj):
        return obj.server.name

    def is_active(self, obj):
        ssh = ssh_connect(
            obj.server.ipv4,
            obj.server.username,
            obj.server.password,
            obj.server.ssh_port,
        )
        is_active = is_inner_port(ssh, obj.port)
        ssh.close()
        return is_active

    def username(self, obj):
        return obj.server.username

    def password(self, obj):
        return obj.server.password

    is_active.short_description = "Is Active"
    is_active.boolean = True


admin.site.register(Alert)


@admin.register(Domain)
class DomainAdminView(admin.ModelAdmin):
    list_display = [
        "id",
        "domain",
        "server",
        "username",
        "password",
        "is_active",
        "to_expire",
        "valid_to",
        "company",
    ]

    def server(self, obj: Domain):
        return obj.server.name

    def username(self, obj: Domain):
        return obj.server.username

    def password(self, obj: Domain):
        return obj.server.password

    def is_active(self, obj: Domain):
        return check_ssl_certificate(obj.domain)["is_valid"]

    def to_expire(self, obj: Domain):
        return (check_ssl_certificate(obj.domain)["valid_to"] - datetime.now()).days

    def valid_to(self, obj: Domain):
        return check_ssl_certificate(obj.domain)["valid_to"]

    def company(self, obj):
        return obj.company.name

    is_active.short_description = "Is Active"
    is_active.boolean = True


@admin.register(Company)
class CompanyAdminView(admin.ModelAdmin):
    list_display = ["name", "chanel_id", "username", "updated", "date_joined"]
    search_fields = ["name", "user__username"]

    def username(self, obj):
        users = obj.user.all().values("username")
        str_ = ""
        for user in users:
            str_ += f"{user['username']} "
        return str_


admin.site.site_header = "Cradle Vision"
admin.site.site_title = "Cradle Vision"
admin.site.index_title = "Dashbord"


celery_models = [
    PeriodicTask,
    IntervalSchedule,
    CrontabSchedule,
    SolarSchedule,
    ClockedSchedule,
    TaskResult,
    GroupResult,
]

# Celery modellarini ro'yxatdan chiqarish
for model in celery_models:
    try:
        admin.site.unregister(model)
    except admin.sites.NotRegistered:
        pass  # Model allaqachon ro'yxatdan chiqarilgan bo'lsa, hech narsa qilmaymiz

# # Modellarni yashirin holda ro'yxatdan o'tkazish
# class HiddenAdmin(admin.ModelAdmin):
#     def has_module_permission(self, request):
#         return False  # Admin modullarni ko'rsatmaydi

# # Modellarni yashirish
# for model in celery_models:
#     admin.site.register(model, HiddenAdmin)
