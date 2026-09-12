export function initTracking() {
  loadPixel();
  loadAnalytics();
  const gpc = (navigator as any).globalPrivacyControl;
  if (gpc) {
    console.log("gpc seen");
  }
}
