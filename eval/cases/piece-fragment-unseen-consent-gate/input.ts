  useEffect(() => {
    analytics.init({ token: ANALYTICS_TOKEN });
    analytics.page();
  }, []);
