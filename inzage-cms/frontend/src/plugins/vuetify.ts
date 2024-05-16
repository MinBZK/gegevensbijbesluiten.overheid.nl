import { createVuetify, ThemeDefinition } from 'vuetify'
import { nl } from 'vuetify/locale'

const beheermodule_theme: ThemeDefinition = {
  colors: {
    primary: '#01689b',
    secondary: '#b3d2e1',
    tertiary: '#d9e8f0',
    quaternary: '#cae3f0',
    quinary: '#d2e5ee',
    accent: '#82B1FF',
    error: '#FF5252',
    info: '#2196F3',
    success: '#4CAF50',
    warning: '#FFC107',
    headerTextColour: '#000000',
    headerHoverColour: '#FCF29A',
  },
}

export default createVuetify({
  theme: {
    defaultTheme: 'beheermodule_theme',
    themes: {
      beheermodule_theme,
    },
    cspNonce: 'eQw4j9WgXcB',
  },
  locale: {
    messages: nl,
  },
})
