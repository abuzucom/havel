export async function registerUser(payload: SignupPayload) {
  const user = await db.users.create({
    email: payload.email,
    displayName: payload.displayName,
  });
  await adPlatform.addToAudience(user.id, payload.interests);
  return user;
}
