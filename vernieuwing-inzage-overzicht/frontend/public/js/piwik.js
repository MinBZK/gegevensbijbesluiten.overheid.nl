export default defineNuxtPlugin((nuxtApp) => {
  nuxtApp.hook('page:finish', () => {
    const userId = usePiwikPro(({ PageViews, GoalConversions, UserManagement }) => {
      PageViews.trackPageView();
      GoalConversions.trackGoal(1, 100);
      return UserManagement.getUserId();
    });
  })
})
