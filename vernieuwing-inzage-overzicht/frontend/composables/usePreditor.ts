import type { SupportingText } from '~~/types/preditor'

export const usePreditor = () => {
  /**
   * Summary. This composable attempts to mirror a part of the i18n module.
   *
   * The i18n module uses a function named 't('path.here')' to do local translation using
   * the locale JSONs. This can be replaced with the 'p('path.here')' function for preditor,
   * Which will look up the indicated path in the supporting text from preditor instead.
   *
   * Description. To migrate to preditor from i18n do the following:
   * const { t } = usei18n() -> const { p } = usePreditor()
   * t('someKeyHere') -> p('someKeyHere')
   */
  const { currentLocale } = useLocale()

  const supportingText = useState<SupportingText | null>('supportingText', () => null)

  const localPrefix = `/${currentLocale.value}`
  // Looks up key in the supporting text. language is based on currentLocale
  const p = (key: string) => {
    if (!supportingText.value) return key

    try {
      const localisedSupportText = supportingText.value[currentLocale.value]
      const value = key
        .split('.')
        .reduce(
          (obj, subKey) => obj[subKey as keyof SupportingText],
          localisedSupportText
        ) as string

      return value.replace('{localised_url}', localPrefix)
    } catch (error) {
      return key
    }
  }

  return {
    p
  }
}
