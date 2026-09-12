export function trackPurchase(user: User, order: Order) {
  adNetwork.send({ email: user.email, value: order.total });
  analytics.send({ userId: user.id, value: order.total });
}
