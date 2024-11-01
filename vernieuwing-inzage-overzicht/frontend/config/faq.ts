export interface Question {
  question: string
  answer_1: string
  answer_2: string
  answer_3?: string
  link_3_text?: string
  link_3_url?: string
  link_4_text?: string
  link_4_url?: string
  link_5_text?: string
  link_5_url?: string
}

// References to locale text
export const questions: Question[] = [
  {
    question: 'faq.1.question',
    answer_1: 'faq.1.answer_1',
    answer_2: 'faq.1.answer_2',
    answer_3: 'faq.1.answer_3',
    link_3_text: 'faq.1.link_3_text',
    link_3_url: 'faq.1.link_3_url'
  },
  {
    question: 'faq.2.question',
    answer_1: 'faq.2.answer_1',
    answer_2: 'faq.2.answer_2'
  },
  {
    question: 'faq.3.question',
    answer_1: 'faq.3.answer_1',
    answer_2: 'faq.3.answer_2',
    answer_3: 'faq.3.answer_3'
  },
  {
    question: 'faq.4.question',
    answer_1: 'faq.4.answer_1',
    answer_2: 'faq.4.answer_2'
  },
  {
    question: 'faq.5.question',
    answer_1: 'faq.5.answer_1',
    answer_2: 'faq.5.answer_2'
  },
  {
    question: 'faq.6.question',
    answer_1: 'faq.6.answer_1',
    answer_2: 'faq.6.answer_2',
    answer_3: 'faq.6.answer_3',
    link_3_text: 'faq.6.link_3_text',
    link_3_url: 'faq.6.link_3_url'
  },
  {
    question: 'faq.7.question',
    answer_1: 'faq.7.answer_1',
    answer_2: 'faq.7.answer_2',
    answer_3: 'faq.7.answer_3',
    link_4_text: 'faq.7.link_4_text',
    link_4_url: 'faq.7.link_4_url',
    link_5_text: 'faq.7.link_5_text',
    link_5_url: 'faq.7.link_5_url'
  }
]
