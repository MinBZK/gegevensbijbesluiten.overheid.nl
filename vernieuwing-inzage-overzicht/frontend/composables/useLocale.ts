export const useLocale = () => {
  const persistentLocale = useCookie('locale')

  const composer = useI18n()

  const setLocale = (locale: string) => {
    persistentLocale.value = locale
    composer.locale.value = locale
  }

  // Because we do not use the browser language, we can set the locale to a fixed value
  // setLocale(persistentLocale.value || 'nl')
  setLocale('nl')

  return { setLocale, currentLocale: composer.locale }
}
