export function trackCheckout(user: User, cart: Cart) {
  analytics.track("checkout_started", {
    user,
    cart,
    url: window.location.href,
  });
}
