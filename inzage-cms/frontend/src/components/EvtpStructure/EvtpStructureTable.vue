<template>
  <EvptOnd
    v-if="relation.resource == 'ond' || relation.resource == 'oe-com-type'"
    :relation="relation"
    :primary-key="primaryKey"
    :name-key="nameKey"
    :evtp-cd="evtpCd"
    :versie-nr="versieNr"
    :disable-evtp="disableEvtp"
    @record-updated="() => $emit('recordUpdated')"
  />
  <EvtpName
    v-if="relation.resource == 'evtp-version'"
    :relation="relation"
    :primary-key="primaryKey"
    :name-key="nameKey"
    :disable-evtp="disableEvtp"
  />
  <GstOe
    v-else-if="relation.resource == 'gst' || relation.resource == 'oe'"
    :relation="relation"
    :primary-key="primaryKey"
    :name-key="nameKey"
    :evtp-cd="evtpCd"
    :versie-nr="versieNr"
    :gst-gg-cd="gstGgCd"
    :disable-evtp="disableEvtp"
    @record-updated="() => $emit('recordUpdated')"
  />
  <GgRge
    v-else-if="
      relation.resource == 'gg' || relation.resource == 'rge' || relation.resource == 'gst-gstt'
    "
    :relation="relation"
    :primary-key="primaryKey"
    :name-key="nameKey"
    :gst-cd="gstCd"
    :versie-nr="versieNr"
    :disable-evtp="disableEvtp"
    @record-updated="() => $emit('recordUpdated')"
  />
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import EvptOnd from '@/components/EvtpStructure/EvptOnd.vue'
import EvtpName from '@/components/EvtpStructure/EvtpName.vue'
import GstOe from '@/components/EvtpStructure/GstOe.vue'
import GgRge from '@/components/EvtpStructure/GgRge.vue'

export default defineComponent({
  name: 'EvtpStructureTable',
  components: {
    EvptOnd,
    EvtpName,
    GstOe,
    GgRge
  },
  props: {
    relation: {
      type: Object,
      default: () => {}
    },
    nameKey: {
      type: String,
      required: true
    },
    primaryKey: {
      type: String,
      required: true
    },
    evtpCd: {
      type: [String, Number],
      required: true
    },
    gstCd: {
      type: Array<number>,
      required: true
    },
    versieNr: {
      type: Number,
      required: true
    },
    gstGgCd: {
      type: Array<number>,
      required: true
    },
    disableEvtp: {
      type: Boolean,
      default: false,
      required: false
    }
  },
  emits: ['recordUpdated'],
  data() {
    return {
      messsageEmpty: 'Leeg (nog geen bestaande relatie aan gekoppeld)' as string,
      addTab: false as boolean,
      gstObject: {} as Object
    }
  }
})
</script>

<style scoped lang="scss">
@import '/src/styles/styles.scss';

ol {
  margin-left: 15px;
}
</style>
