from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

from fashionapp import views

urlpatterns = [
    # path('', views.home),
    path('', views.ProdutView.as_view(), name="home"),
    path('address', views.ProfileAddress, name="address"),
    path('showcart', views.ShowCart, name="showcart"),
    path('cartview', views.cartview, name="cartview"),
    path('pluscart', views.plus_cart),
    path('paymentdone', views.payment_done, name="paymentdone"),
    path('emptycart', views.emptycartview, name="emptycart"),
    path('minuscart', views.minus_cart),
    path('removecart', views.remove_cart),
    path('base', views.base, name="base"),
    path('buynow', views.buynow, name="buynow"),
    # path('product-detail', views.productdetail, name="product-detail"),
    path('productdetail/<int:pk>', views.ProductDetailView.as_view(), name="productdetail"),
    path('product', views.allproducts, name="product"),
    path('product/<slug:data>', views.allproducts, name="productdata"),
    path('login/', views.LoginView, name="login"),
    path('logout', views. LogoutView, name="logout"),
    path('profile', views.Profile, name="profile"),
    path('orders', views.orderView, name="orders"),
    path('checkout', views.checkoutView, name="checkout"),
    path('changepassword', views.Changepassword, name="changepassword"),
    path('blog', views.blogview, name="blog"),
    path('news', views.newsview, name="news"),
    path('register', views.CustomerRegistrationView, name="register"),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

