import type { OndTree } from '@/types/Ond'
import type { OeComTypeTree } from '@/types/Oe'
import type { Omg } from '@/types/EvtpVersion'

const evtpCd = (record) => {
  return record['evtp_cd']
}

const versieNr = (record) => {
  return record['versie_nr']
}

const evtpGst = (record) => {
  try {
    const evtp_gst = record.entities_evtp_gst.map((evtp_gst) => ({
      evtp_gst_cd: evtp_gst.evtp_gst_cd,
      sort_key: evtp_gst.sort_key || 1000
    }))
    return evtp_gst
  } catch {
    return null
  }
}

const gst = (record) => {
  try {
    const gst = record.entities_evtp_gst.map((evtp_gst) => evtp_gst.entity_gst)
    gst.map((gst, index) => (gst['evtp_gst_cd'] = record.entities_evtp_gst[index].evtp_gst_cd))
    gst.map(
      (gst, index) => (gst['entities_gst_gstt'] = record.entities_evtp_gst[index].entities_gst_gstt)
    )
    gst.map(
      (gst, index) => (gst['entities_gst_rge'] = record.entities_evtp_gst[index].entities_gst_rge)
    )
    return gst
  } catch {
    return null
  }
}

const ond = (record): OndTree[] => {
  try {
    const ond = record.entities_evtp_ond.map((item) => item.entity_ond)
    ond.map((ond, index) => (ond['evtp_ond_cd'] = record.entities_evtp_ond[index].evtp_ond_cd))
    return ond
  } catch {
    return []
  }
}

const oeComType = (record): OeComTypeTree[] => {
  try {
    const oeComType = record.entities_evtp_oe_com_type.map((item) => item.entity_oe_com_type)
    oeComType.map(
      (oeComType, index) =>
        (oeComType['evtp_oe_com_type_cd'] =
          record.entities_evtp_oe_com_type[index].evtp_oe_com_type_cd)
    )
    return oeComType
  } catch {
    return []
  }
}

const omg = (record): Omg | '' => {
  try {
    const omg = record.entity_omg
    return omg
  } catch {
    return ''
  }
}

const gstCd = (record) => {
  try {
    const gstCd = record.entities_evtp_gst.map((evtp_gst) => evtp_gst.entity_gst.gst_cd)
    return gstCd
  } catch {
    return null
  }
}

const gstGgCd = (record) => {
  try {
    const gstGgCd = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.map((gst_gg) => gst_gg.gst_gg_cd)
    )
    return gstGgCd
  } catch {
    return null
  }
}

const gstGstType = (record) => {
  try {
    const evtpGst = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gstt.map((gst_gstt) => gst_gstt.entity_gst_type)
    )

    const gst_gstt_cd_list = record.entities_evtp_gst.map((item) =>
      item.entities_gst_gstt.map((gst_gstt) => gst_gstt.gst_gstt_cd)
    )
    evtpGst.forEach((object, index) =>
      object.map(
        (evtpGst, subIndex) => (evtpGst['gst_gstt_cd'] = gst_gstt_cd_list[index][subIndex])
      )
    )
    return evtpGst
  } catch (error) {
    return []
  }
}

const oeBron = (record) => {
  try {
    const orgEenheidBron = record.entities_evtp_gst.map(
      (evtp_gst) => evtp_gst.entity_gst.entity_oe_bron
    )
    return orgEenheidBron
  } catch {
    return null
  }
}

const oeBest = (record) => {
  try {
    const orgEenheidBest = record.entities_evtp_gst.map(
      (evtp_gst) => evtp_gst.entity_gst.entity_oe_best
    )
    return orgEenheidBest
  } catch {
    return null
  }
}

const ibron = (record) => {
  try {
    const ibronGstOrgEenheid = record.entities_evtp_gst.map(
      (evtp_gst) => evtp_gst.entity_gst.entity_ibron
    )
    return ibronGstOrgEenheid
  } catch {
    return null
  }
}

const ggChild = (record) => {
  try {
    record.entities_evtp_gst.forEach((evtp_gst) =>
      evtp_gst.entities_gst_gg.forEach((gst_gg) => {
        gst_gg.entity_gg['gst_gg_cd'] = gst_gg.gst_gg_cd
        gst_gg.entity_gg['sort_key'] = gst_gg.sort_key || 1000
      })
    )

    const gg = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.map((gst_gg) => gst_gg.entity_gg)
    )

    gg.forEach((ggList) => {
      ggList.sort((a, b) => {
        if (a.sort_key === b.sort_key) {
          return a.omschrijving.localeCompare(b.omschrijving)
        }
        return a.sort_key - b.sort_key
      })
    })

    return gg
  } catch {
    return null
  }
}

const ggParent = (record) => {
  try {
    const ggParent = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.map((gst_gg) =>
        gst_gg.entity_gg.count_parents === 1
          ? gst_gg.entity_gg.parent_entities[0].parent_entity
          : null
      )
    )
    return ggParent
  } catch {
    return null
  }
}

const rge = (record) => {
  try {
    const rge = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_rge.map((gst_rge) => gst_rge.entity_rge)
    )

    const gst_rge_cd_list = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_rge.map((gst_rge) => gst_rge.gst_rge_cd)
    )
    const gst_rge_sort_key = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_rge.map((gst_rge) => gst_rge.sort_key || 1000)
    )
    rge.forEach((object, index) =>
      object.forEach((rge, subIndex) => {
        rge['gst_rge_cd'] = gst_rge_cd_list[index][subIndex]
        rge['sort_key'] = gst_rge_sort_key[index][subIndex]
      })
    )

    rge.forEach((ggList) => {
      ggList.sort((a, b) => {
        if (a.sort_key === b.sort_key) {
          return a.titel.localeCompare(b.titel)
        }
        return a.sort_key - b.sort_key
      })
    })

    return rge
  } catch {
    return null
  }
}

export {
  gstGstType,
  ond,
  oeComType,
  omg,
  evtpCd,
  versieNr,
  gst,
  oeBron,
  oeBest,
  ggChild,
  rge,
  ggParent,
  ibron,
  gstCd,
  gstGgCd,
  evtpGst
}
