"""
URL configuration for co_working_space_booking_system_api project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/users/', include('users.urls')),
    path('api/working-spaces/', include('working_spaces.urls')),
    path('api/', include('space_bookings.urls')),
]

# Custom error handlers
handler400 = 'utils.exception_handler.bad_request_handler'
handler403 = 'utils.exception_handler.permission_denied_handler'
handler404 = 'utils.exception_handler.page_not_found_handler'
handler500 = 'utils.exception_handler.internal_server_error_handler'
