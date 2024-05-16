const evtpCd = (record) => {
  return record['evtp_cd']
}

const versieNr = (record) => {
  return record['versie_nr']
}

const gst = (record) => {
  try {
    const gst = record.entities_evtp_gst.map((evtp_gst) => evtp_gst.entity_gst)
    gst.map(
      (gst, index) =>
        (gst['evtp_gst_cd'] = record.entities_evtp_gst[index].evtp_gst_cd)
    )
    gst.map(
      (gst, index) =>
        (gst['conditie'] = record.entities_evtp_gst[index].conditie)
    )
    return gst
  } catch {
    return null
  }
}

const ond = (record) => {
  try {
    const ond = record.entities_evtp_ond.map((item) => item.entity_ond)
    ond.map(
      (ond, index) =>
        (ond['evtp_ond_cd'] = record.entities_evtp_ond[index].evtp_ond_cd)
    )
    return ond
  } catch {
    return null
  }
}


const gstCd = (record) => {
  try {
    const gstCd = record.entities_evtp_gst.map(
      (evtp_gst) => evtp_gst.entity_gst.gst_cd
    )
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

const gstGsttype = (record) => {
  try {
    const evtpGst = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entity_gst.entities_gst_gstt.map((gst_gstt) => gst_gstt.entity_gsttype)
    )

    const gst_gstt_cd_list = record.entities_evtp_gst.map((item) =>
      item.entity_gst
    .entities_gst_gstt.map((gst_gstt) => gst_gstt.gst_gstt_cd)
    )
    evtpGst.forEach((object, index) =>
      object.map(
        (evtpGst, subIndex) => (evtpGst['gst_gstt_cd'] = gst_gstt_cd_list[index][subIndex])
      )
    )
    return evtpGst

  } catch (error){
    return null
  }
}

const orgEenheidBron = (record) => {
  try {
    const orgEenheidBron = record.entities_evtp_gst.map(
      (evtp_gst) => evtp_gst.entity_gst.entity_oe_bron
    )
    return orgEenheidBron
  } catch {
    return null
  }
}

const orgEenheidBest = (record) => {
  try {
    const orgEenheidBest = record.entities_evtp_gst.map(
      (evtp_gst) => evtp_gst.entity_gst.entity_oe_best
    )
    return orgEenheidBest
  } catch {
    return null
  }
}

const ibronOrgEenheidBest = (record) => {
  try {
    const ibronOrgEenheidBest = record.entities_evtp_gst
      .filter((evtp_gst) => evtp_gst.entity_gst.entity_oe_best.ibron)
      .map((evtp_gst) => evtp_gst.entity_gst.entity_oe_best.ibron.Oe)
    return ibronOrgEenheidBest
  } catch {
    return null
  }
}

const ibronOrgEenheidBron = (record) => {
  try {
    const ibronOrgEenheidBron = record.entities_evtp_gst
      .filter((evtp_gst) => evtp_gst.entity_gst.entity_oe_bron.ibron)
      .map((evtp_gst) => evtp_gst.entity_gst.entity_oe_bron.ibron.Oe)
    return ibronOrgEenheidBron
  } catch {
    return null
  }
}

const ibronGstOrgEenheid = (record) => {
  try {
    const ibronGstOrgEenheid = record.entities_evtp_gst
      .filter((evtp_gst) => evtp_gst.entity_gst.ibron)
      .map((evtp_gst) => evtp_gst.entity_gst.ibron.Oe)
    return ibronGstOrgEenheid
  } catch {
    return null
  }
}

const ibronGstGgOrgEenheid = (record) => {
  try {
    const ibronGstGgOrgEenheid = record.entities_evtp_gst
      .filter((evtp_gst) => evtp_gst.entity_gst.ibron)
      .map((evtp_gst) =>
        evtp_gst.entity_gst.entities_gst_gg.map((gst_gg) => gst_gg.ibron.Oe)
      )
    return ibronGstGgOrgEenheid
  } catch {
    return null
  }
}

const ibronRgeOrgEenheid = (record) => {
  try {
    const ibronRgeOrgEenheid = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.map((gst_gg) => gst_gg.entity_rge.ibron.Oe)
    )
    return ibronRgeOrgEenheid
  } catch {
    return null
  }
}

const ibronGgHogerOrgEenheid = (record) => {
  try {
    const ibronGgHogerOrgEenheid = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.NTITIES_gst_gg.entity_gg.parent_entities.map((parent_entities) =>
        parent_entities.parent_entity.ibron
          ? parent_entities.parent_entity.ibron.Oe
          : null
      )
    )
    return ibronGgHogerOrgEenheid
  } catch {
    return null
  }
}

const ibronGgOrgEenheid = (record) => {
  try {
    const ibronGgOrgEenheid = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.entity_gg.ibron
        ? evtp_gst.entities_gst_gg.entity_gg.ibron.Oe
        : null
    )
    return ibronGgOrgEenheid
  } catch {
    return null
  }
}

const gg = (record) => {
  try {
    const gg = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.map((gst_gg) => gst_gg.entity_gg)
    )

    const gst_gg_cd_list = record.entities_evtp_gst.map((evtp_gst) =>
      evtp_gst.entities_gst_gg.map((gst_gg) => gst_gg.gst_gg_cd)
    )

    gg.forEach((object, index) =>
      object.map(
        (gg, subIndex) => (gg['gst_gg_cd'] = gst_gg_cd_list[index][subIndex])
      )
    )

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

    rge.forEach((object, index) =>
      object.map(
        (rge, subIndex) =>
          (rge['gst_rge_cd'] = gst_rge_cd_list[index][subIndex])
      )
    )
    return rge
  } catch {
    return null
  }
}

export {
  gstGsttype,
  ond,
  evtpCd,
  versieNr,
  gst,
  orgEenheidBron,
  orgEenheidBest,
  gg,
  rge,
  ggParent,
  ibronGstOrgEenheid,
  ibronOrgEenheidBest,
  ibronOrgEenheidBron,
  ibronGstGgOrgEenheid,
  ibronRgeOrgEenheid,
  ibronGgHogerOrgEenheid,
  ibronGgOrgEenheid,
  gstCd,
  gstGgCd,
}
