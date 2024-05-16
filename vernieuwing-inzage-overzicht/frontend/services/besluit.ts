import type {
  EvtpGst,
  EvtpGg,
  EvtpQuery,
  EvtpQueryResult,
  Evtp,
} from '~~/types/besluit'

const getEvtpByOnd = (OndCd: number) =>
  useFetch<Evtp[]>(`/ond/${OndCd}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getEvtpFiltered = (query: EvtpQuery) =>
  useFetch<EvtpQueryResult>('/evtp/filter', {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
    method: 'POST',
    body: query,
  })

const getOneEvtpGgVersion = (evtpUpc: string, evtpVersionNr: number) =>
  useFetch<EvtpGg>(`/evtp-tree/${evtpUpc}/${evtpVersionNr}/gg/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getOneEvtpGg = (evtpUpc: string) =>
  useFetch<EvtpGg>(`/evtp-tree/${evtpUpc}/gg/`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getOneEvtpGstVersion = (
  evtpUpc: string,
  evtpVersionNr: number,
  gstUpc: string
) =>
  useFetch<EvtpGst>(`/evtp-tree/${evtpUpc}/${evtpVersionNr}/gst/${gstUpc}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const getOneEvtpGst = (evtpUpc: string, gstUpc: string) =>
  useFetch<EvtpGst>(`/evtp-tree/${evtpUpc}/gst/${gstUpc}`, {
    baseURL: useRuntimeConfig().public.apiBaseUrl,
  })

const downloadUrl = () => `${useRuntimeConfig().public.apiBaseUrl}/evtp/file`

export default {
  getEvtpFiltered,
  getOneEvtpGgVersion,
  getOneEvtpGg,
  getOneEvtpGstVersion,
  getOneEvtpGst,
  downloadUrl,
  getEvtpByOnd,
}
