<template>
  <v-timeline
    side="end"
    direction="horizontal"
  >
    <v-timeline-item
      v-for="(relation, index) in relations"
      :key="index"
      :dot-color="relation.color"
      size="small"
      :icon="relation.icon"
      width="100%"
    >
      <template #opposite>
        <br>
        <router-link
          :to="{ name: 'table', params: { resource: relation.resource } }"
        >
          <th>{{ relation.label }}</th>
        </router-link>
      </template>
      <v-table class="row-height-50">
        <tbody
          v-if="recordLoaded"
          class="table-responsive"
        >
          <EvtpStructureTable
            :relation="relation"
            :primary-key="relation.primaryKey"
            :name-key="relation.nameKey"
            :evtp-cd="evtpCd"
            :gst-cd="getGstCd"
            :versie-nr="getVersieNr"
            :gst-gg-cd="getGstGgCd"
            :disable-evtp="disableEvtp"
            @record-updated="() => getEvtpStructure()"
          />
        </tbody>
        <tbody v-else>
          <td
            class="centered"
            style="overflow: hidden"
          >
            <v-progress-circular
              indeterminate
              color="primary"
            />
          </td>
        </tbody>
      </v-table>
    </v-timeline-item>
  </v-timeline>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { tables } from '@/config/tables'
import axios from 'axios'
import store from '@/store/index'
import {
  gstGsttype,
  ond,
  gst,
  orgEenheidBron,
  orgEenheidBest,
  gg,
  rge,
  ggParent,
  gstCd,
  versieNr,
  gstGgCd,
} from '@/util/flatEvtpTree'
import EvtpStructureTable from '@/components/EvtpStructure/EvtpStructureTable.vue'

export default defineComponent({
  name: 'EvtpStructureOverview',
  components: {
    EvtpStructureTable,
  },
  props: {
    record: {
      type: Object,
      default: () => {},
    },
    recordLoaded: {
      type: Boolean,
      default: () => true,
    },
    resource: {
      type: String,
      required: true,
    },
    evtpCd: {
      type: [String, Number],
      required: true,
    },
    versieNr: {
      type: [Number, String],
      default: null,
      required: false,
    },
    disableEvtp: {
      type: Boolean,
      default: false,
      required: false,
    },
  },
  data() {
    return {
      addTab: false as boolean,
      gstObject: {} as Object,
      recordRelation: {} as Object,
    }
  },
  computed: {
    getGstGgCd() {
      return gstGgCd(this.recordRelation)
    },
    getGstCd() {
      return gstCd(this.recordRelation)
    },
    getVersieNr() {
      return versieNr(this.recordRelation)
    },
    relations() {
      interface Entity {
        resource: string
        values: Array<object>
        label: string
        icon: string
        color: string
        nameKey: string
        primaryKey: string
      }

      const relations: Array<Entity> = [
        {
          resource: 'evtp-version',
          values: [this.recordRelation],
          label: 'Geselecteerde besluit',
          icon: 'mdi-star',
          color: 'primary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'ond',
          values: ond(this.recordRelation),
          label: 'onderwerp',
          icon: 'mdi-waves-arrow-right',
          color: 'secondary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'gst',
          values: gst(this.recordRelation),
          label: 'gegevensstromen',
          icon: 'mdi-waves-arrow-right',
          color: 'secondary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'gst-gstt',
          values: gstGsttype(this.recordRelation),
          label: 'gegevensstroom type',
          icon: 'mdi-home-group',
          color: 'tertiary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'oe',
          values: orgEenheidBron(this.recordRelation),
          label: 'bron organisaties',
          icon: 'mdi-home-group',
          color: 'tertiary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'oe',
          values: orgEenheidBest(this.recordRelation),
          label: 'afnemende organisaties',
          icon: 'mdi-home-group',
          color: 'tertiary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'rge',
          values: rge(this.recordRelation),
          label: 'regelingen',
          icon: 'mdi-clipboard-check-multiple-outline',
          color: 'quinary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'gg',
          values: gg(this.recordRelation),
          label: 'gegevensgroepen',
          icon: 'mdi-group',
          color: 'quaternary',
          nameKey: '',
          primaryKey: '',
        },
        {
          resource: 'gg',
          values: ggParent(this.recordRelation),
          label: 'hogere gegevensgroepen',
          icon: 'mdi-group',
          color: 'quaternary',
          nameKey: '',
          primaryKey: '',
        },
      ]
      for (let relation of relations) {
        for (let table of tables) {
          if (relation.resource == table.resource) {
            relation.nameKey = table.nameKey
            relation.primaryKey = table.primaryKey
          }
        }
      }
      return relations
    },
  },
  watch: {
    record() {
      this.recordRelation = this.record
    },
  },
  methods: {
    async getEvtpStructure() {
      const { data } = await axios.get(
        `${store.state.APIurl}/${this.resource}/relations/${this.evtpCd}/${this.versieNr}`
      )
      this.recordRelation = data
    },
  },
})
</script>

<style scoped lang="scss">
@import '/src/styles/styles.scss';

ol {
  margin-left: 15px;
}

.row-height-50 {
  border: 1px;
  width: calc(60vh);
  height: calc(100vh);
}
</style>
