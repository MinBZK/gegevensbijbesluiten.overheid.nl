import { useDisplay } from 'vuetify'

export const useMobileBreakpoint = () => {
  return {
    large: useDisplay().mdAndDown,
    medium: useDisplay().smAndDown,
    small: useDisplay().xs,
  }
}
