export function featureFlags(user: User) {
  return {
    recommendations: !user.optedOutOfSale,
    savedSearches: !user.optedOutOfSale,
    prioritySupport: !user.optedOutOfSale,
  };
}
