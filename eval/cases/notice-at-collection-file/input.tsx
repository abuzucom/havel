export function WaitlistForm() {
  return (
    <form action="/api/waitlist" method="post">
      <input name="email" type="email" required />
      <input name="phone" type="tel" />
      <input name="company" />
      <button type="submit">Join</button>
    </form>
  );
}
