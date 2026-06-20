import { createI18n } from 'vue-i18n'
import messages from 'src/i18n/index'

export default ({ app }) => {
  const i18n = createI18n({
    legacy: false,
    locale: 'en',  // default
    fallbackLocale: 'en',
    messages
  })

  app.use(i18n)
}
