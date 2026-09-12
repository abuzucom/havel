export const router = Router();

router.post("/account/delete", requireAuth, async (req, res) => {
  await db.users.delete(req.user.id);
  res.json({ deleted: true });
});
