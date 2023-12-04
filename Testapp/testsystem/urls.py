from django.urls import path

from . import views

app_name = "testsystem"

urlpatterns = [
    path(
        "",
        views.Dashboard.as_view(),
        name="dashboard"),
    path(
        "test/<int:test_id>/",
        views.TestView.as_view(),
        name="test_page"),
    path(
        "test/<int:test_id>/results/",
        views.ResultView.as_view(),
        name="result_page")]
