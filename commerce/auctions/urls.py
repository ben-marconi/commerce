from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("newlisting", views.new_listing, name="newlisting"),
    path("item/<int:item_id>", views.item, name="item"),
    path("closed_item/<int:item_id>", views.closed, name="closed"),
    path("item/bid/<int:item_id>", views.bid, name="bid"),
    path("categories", views.category, name="category"),
    path("categories/<int:category_id>", views.type, name="type"),
    path("item/watchlist/<int:item_id>", views.watchlist, name="watchlist"),
    path("my_watchlist", views.mywatchlist, name="my_watchlist"),
    path("item/comment/<int:item_id>", views.comment, name="comment")
]
