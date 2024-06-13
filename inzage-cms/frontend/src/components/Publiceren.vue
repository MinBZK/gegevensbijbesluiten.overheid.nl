<template>
  <v-container>
    <v-row>
      <v-col>
        <v-autocomplete
          v-if="!loadingInit"
          v-model="searchQuery"
          :label="defaultText"
          :items="evtpsForAutocomplete"
          return-object
          clearable
          hide-no-data
        />
      </v-col>
    </v-row>
    <v-row>
      <v-col cols="3">
        <v-card elevation="1">
          <v-toolbar><v-toolbar-title>Status</v-toolbar-title></v-toolbar>
          <v-list>
            <v-list-subheader class="status-header">
              <b>Status besluit</b>
            </v-list-subheader>
            <v-list-item :class="getStatusColorClass(evtpStatus)">
              {{ evtpStatus }}
            </v-list-item>
            <v-list-subheader><b>Versie nummer</b></v-list-subheader>
            <v-list-item>
              {{ searchQuery?.versie }}
            </v-list-item>
            <v-list-subheader><b>Huidige versie</b></v-list-subheader>
            <v-list-item>
              {{ evtpCurrentVersion ? 'Ja' : 'Nee' }}
            </v-list-item>
          </v-list>
          <v-toolbar><v-toolbar-title>Acties</v-toolbar-title></v-toolbar>
          <v-list>
            <v-list-subheader>
              <b v-if="evtpUpgradeButton.text == getStatusPubliceren">Promoveer het besluit óók in publiek</b>
              <b v-else-if="evtpUpgradeButton.text == getStatusGereedVoorControle">Promoveer het besluit alleen in concept</b>
              <b v-else>Gepubliceerd in publiek</b>
            </v-list-subheader>
            <v-list-item dense>
              <v-btn
                :disabled="evtpUpgradeButton.disabled"
                width="1000"
                class="action-buttons"
                color="green-lighten-2"
                @click="upgradeEvtp"
              >
                <v-icon v-if="!evtpUpgradeButton.hideIcons">
                  mdi-arrow-right-thin
                </v-icon>{{ evtpUpgradeButton.text }}
                <v-icon v-if="!evtpUpgradeButton.hideIcons">
                  {{ evtpUpgradeButton.icon }}
                </v-icon>
              </v-btn>
            </v-list-item>
            <v-divider />
            <v-divider insert />
            <v-list-subheader>
              <b>Degradeer het besluit naar nieuw</b>
            </v-list-subheader>
            <v-list-item>
              <v-btn
                class="action-buttons"
                color="warning"
                @click="resetEvtpStatus"
              >
                Reset Besluit Status
              </v-btn>
            </v-list-item>
            <v-divider />
            <v-list-subheader><b>Archiveer het besluit</b></v-list-subheader>
            <v-list-item>
              <v-btn
                class="action-buttons"
                color="error"
                @click="archiveEvtpStatus"
              >
                Archiveer besluit
              </v-btn>
            </v-list-item>
          </v-list>
        </v-card>
      </v-col>
      <v-col>
        <v-card
          rounded="true"
          elevation="1"
        >
          <v-toolbar>
            <v-toolbar-title>
              {{ searchQuery?.title || defaultText }}
            </v-toolbar-title>
            <v-spacer />
          </v-toolbar>
          <v-card-item v-if="loading">
            <div class="centered">
              <v-progress-circular
                indeterminate
                color="primary"
              />
            </div>
          </v-card-item>
          <v-card-item>
            <v-list v-if="!loading && searchQuery">
              <v-list-item>
                <b>Validatie regels</b>
              </v-list-item>
              <v-list-group
                v-for="(table, indexTable) in flattenedDataRules"
                :key="indexTable"
              >
                <template #activator="{ props }">
                  <v-list-item
                    :disabled="table.result == false"
                    v-bind="props"
                    :title="`Regel ${table.rule}: ${table.name}`"
                  >
                    <template #append>
                      <v-row>
                        <v-col :style="`width:56px`" /><v-icon
                          id="column-header"
                          :color="table.result ? 'red' : 'green'"
                        >
                          {{ `${table.result ? 'mdi-close' : 'mdi-check'}` }}
                        </v-icon>
                      </v-row>
                    </template>
                    <template #prepend />
                  </v-list-item>
                </template>
                <v-list-item class="header-list-item">
                  <v-row>
                    <v-col cols="5">
                      <h5>Beschrijving</h5>
                    </v-col>
                    <v-col cols="7">
                      <h5>Foutmelding(en)</h5>
                    </v-col>
                  </v-row>
                </v-list-item>
                <v-divider inset />
                <v-list-item>
                  <v-row>
                    <v-col cols="5">
                      {{ table.explanation }}
                    </v-col>
                    <v-col cols="7">
                      <ol>
                        <li
                          v-for="(row, indexRow) in table.content"
                          :key="indexRow"
                        >
                          {{ row['feedback_message'] }}
                        </li>
                      </ol>
                    </v-col>
                  </v-row>
                </v-list-item>
              </v-list-group>
            </v-list>
          </v-card-item>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <v-snackbar
    v-model="snackbarSuccess"
    color="success"
    timeout="1500"
  >
    Publicatie is gelukt!
    <template #actions>
      <v-btn @click="snackbarSuccess = false">
        Sluiten
      </v-btn>
    </template>
  </v-snackbar>
  <v-snackbar
    v-model="snackbarError"
    color="red"
    timeout="1500"
  >
    Publicatie is mislukt...
    {{ snackbarMessage }}
    <template #actions>
      <v-btn @click="snackbarError = false">
        Sluiten
      </v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import axios from 'axios'
import { defineComponent } from 'vue'
import store from '@/store/index'
import { EvtpVersion } from '@/types/EvtpVersion'
import { PublicatieStatus, getPublicatieStatus } from '@/types/PublicatieStatus'

export default defineComponent({
  name: 'OE',
  data() {
    return {
      selected: [] as Array<{ table: any; row: any }>,
      evtpData: {} as EvtpVersion,
      evtpDataRules: {
        type: Object,
        default: () => {},
      },
      flattenedDataRules: [] as Array<{
        rule: string
        name: string
        explanation: string
        importance: string
        result: boolean
        content: object
      }>,
      loading: false,
      loadingInit: false,
      snackbarSuccess: false,
      snackbarError: false,
      snackbarMessage: '',
      searchQuery: { title: '' } as {
        title: string
        value: string
        versie: number
      },
      evtpList: [] as object[],
      envObj: [] as Array<object>,
      urlConcept: '' as string,
      url: '' as string,
      passedRules: false as boolean,
      defaultText: 'Selecteer een besluit' as string,
    }
  },
  computed: {
    getStatusPubliceren() {
      return PublicatieStatus.GEPUBLICEERD
    },
    getStatusGereedVoorControle() {
      return PublicatieStatus.GEREEDVOORCONTROLE
    },
    evtpsForAutocomplete() {
      return this.evtpList?.map((obj) => ({
        title: `${obj['evtp_nm']} (${obj['evtp_cd']}) versie: ${obj['versie_nr']} - ${getPublicatieStatus(obj['id_publicatiestatus'])}`,
        value: obj['evtp_cd'],
        versie: obj['versie_nr'],
      }))
    },
    statusData() {
      interface StatusData {
        number: number
        icon: string
        label: string
      }
      const statusData: Array<StatusData> = [
        {
          number: 1,
          icon: 'mdi-magnify',
          label: PublicatieStatus.NIEUW,
        },
        {
          number: 2,
          icon: 'mdi-check',
          label: PublicatieStatus.GEREEDVOORCONTROLE
        },
        {
          number: 3,
          icon: 'mdi-eye',
          label: PublicatieStatus.GEPUBLICEERD,
        },
        {
          number: 4,
          icon: 'mdi-check',
          label: PublicatieStatus.GEARCHIVEERD,
        },
      ]
      return statusData
    },
    evtpUpgradeButton() {
      const evtpStatus = this.evtpData.id_publicatiestatus
      if (evtpStatus == 3 && this.passedRules) {
        return {
          hideIcons: true,
          icon: 'mdi-folder',
          text: 'Al gepubliceerd!',
          disabled: true,
        }
      } else if (this.passedRules === false && evtpStatus) {
        return {
          hideIcons: true,
          icon: 'mdi-folder',
          text: 'Niet alle regels zijn voldaan!',
          disabled: true,
        }
      } else if (!evtpStatus) {
        return {
          hideIcons: true,
          icon: 'mdi-folder',
          text: this.defaultText,
          disabled: true,
        }
      }

      const statusInfo = this.statusData.filter(
        (status) => status.number == evtpStatus + 1
      )[0]
      if (statusInfo == undefined) {
        return {
          hideIcons: true,
          icon: 'mdi-folder',
          text: PublicatieStatus.GEARCHIVEERD,
          disabled: true,
        }
      } else {
        // test if the button should be disabled
        let disabled = false
        return {
          hideIcons: false,
          icon: statusInfo.icon,
          text: statusInfo.label,
          disabled: disabled,
        }
      }
    },
    evtpStatus() {
      return (
        this.statusData.filter(
          (status) => status.number == this.evtpData.id_publicatiestatus
        )[0]?.label || PublicatieStatus.GEARCHIVEERD
      )
    },
    evtpCurrentVersion() {
      return this.evtpData?.huidige_versie
    },
  },
  watch: {
    searchQuery() {
      this.getEvtpDataAndValidate(
        this.searchQuery?.value,
        this.searchQuery?.versie
      )
      this.selected = []
    },
  },
  async created() {
    this.init()
  },
  methods: {
    getStatusColorClass(status) {
      switch (status) {
        case PublicatieStatus.NIEUW:
          return 'status-new'
        case PublicatieStatus.GEREEDVOORCONTROLE:
          return 'status-draft'
        case PublicatieStatus.GEPUBLICEERD:
          return 'status-published'
        case PublicatieStatus.GEARCHIVEERD:
          return 'status-archived'
        default:
          return ''
      }
    },
    flattenedEvtpRules() {
      this.flattenedDataRules = [] as Array<{
        rule: string
        name: string
        explanation: string
        importance: string
        result: boolean
        content: object
      }>
      let lengthRules = Object.keys(this.evtpDataRules).length
      for (let i = 0; i < lengthRules; i++) {
        this.flattenedDataRules.push({
          rule: this.evtpDataRules[i]?.['ruleId'],
          name: this.evtpDataRules[i]?.['name'],
          explanation: this.evtpDataRules[i]?.['explanation'],
          importance: this.evtpDataRules[i]?.['importance'],
          result: this.evtpDataRules[i]?.['result'],
          content: this.evtpDataRules[i]?.['content'],
        })
      }
      this.passedAllRules()
    },
    passedAllRules() {
      if (
        this.flattenedDataRules.every((rule) => rule.result === false) &&
        this.flattenedDataRules.length > 0
      ) {
        this.passedRules = true
      } else {
        this.passedRules = false
      }
    },
    async init() {
      await this.getEvtpList()
    },
    async getEvtpList() {
      this.loadingInit = true
      const { data } = await axios.get(
        `${store.state.APIurl}/evtp-version-list-versions/`
      )
      this.evtpList = data
      this.loadingInit = false
    },
    async getEvtpDataAndValidate(evtp_cd: number | string, versie_nr: number) {
      if (evtp_cd) {
        const objectEVTPTree = []
        this.loading = true

        await Promise.all(
          [
            `${store.state.APIurl}/evtp-version/partial/${evtp_cd}/${versie_nr}`,
            `${store.state.APIurl}/evtp-version/relations-validate/${evtp_cd}/${versie_nr}`,
          ].map((endpoint) => axios.get(endpoint))
        )
          .then(function (results) {
            for (let result of results) {
              // @ts-ignore
              objectEVTPTree.push(result.data)
            }
          })
          .finally(() => {
            this.loading = false
            this.evtpData = objectEVTPTree[0] as EvtpVersion
            this.evtpDataRules = objectEVTPTree[1]
            this.flattenedEvtpRules()
          })
      }
    },
    flattenTable(table) {
      // some tables are nested in arrays, these need to be flattened, so that they can be viewed like other tables.
      let flatTable = []
      table?.forEach((nestedTable) => {
        flatTable = flatTable.concat(nestedTable)
      })
      flatTable = flatTable.filter((row) => row != null)
      return flatTable
    },
    getTableStatistics(values) {
      const stat = { total: 0, statusSum: [0] }
      if (values != null && values.length != 0) {
        stat.total = values.length
        for (let status of [0, 1, 2, 3, 4, 5]) {
          stat.statusSum[status] = values.filter(
            (row) => row.id_publicatiestatus == status
          ).length
        }
      }
      return stat
    },
    itemClicked(table, row) {
      const activeStatus = this.activeStatus(table, row)
      if (activeStatus.isActive) {
        const index = this.selected.indexOf(activeStatus.entityInSelected)
        if (index > -1) {
          this.selected.splice(index, 1)
        }
      } else {
        this.selected.push({ table: table, row: row })
      }
    },
    activeStatus(table: any, row: any) {
      const entityInSelected = this.selected.find(
        (i) =>
          i.table?.resource == table.resource &&
          i.row[table.config.primaryKey] == row[table.config.primaryKey]
      )!
      return {
        isActive: entityInSelected != undefined,
        entityInSelected: entityInSelected,
      }
    },
    async upgradeEvtp() {
      if (this.evtpData && this.evtpData.id_publicatiestatus !== undefined) {
        this.evtpData.id_publicatiestatus++

        await axios({
          method: 'PUT',
          url: `${store.state.APIurl}/evtp-version/change_id_pub/${this.evtpData.evtp_cd}/${this.evtpData.versie_nr}`,
          data: this.evtpData,
        })
        await this.getEvtpDataAndValidate(
          this.evtpData.evtp_cd,
          this.evtpData.versie_nr
        )
      }
    },
    async resetEvtpStatus() {
      this.evtpData.id_publicatiestatus = 1
      await axios({
        method: 'PUT',
        url: `${store.state.APIurl}/evtp-version/change_id_pub/${this.evtpData.evtp_cd}/${this.evtpData.versie_nr}`,
        data: this.evtpData,
      })
      await this.getEvtpDataAndValidate(
        this.evtpData.evtp_cd,
        this.evtpData.versie_nr
      )
    },
    async archiveEvtpStatus() {
      this.evtpData.id_publicatiestatus = 4
      await axios({
        method: 'PUT',
        url: `${store.state.APIurl}/evtp-version/change_id_pub/${this.evtpData.evtp_cd}/${this.evtpData.versie_nr}`,
        data: this.evtpData,
      })
      await this.getEvtpDataAndValidate(
        this.evtpData.evtp_cd,
        this.evtpData.versie_nr
      )
    },
  },
})
</script>

<style scoped>
@import '/src/styles/styles.scss';
.page-link:focus {
  outline: unset;
  border: unset;
}
.scroll {
  overflow-y: scroll;
}
.tile {
  border-radius: 0.1px;
  max-height: 55px;
  overflow: hidden;
}
.tile:hover {
  background: lightgray;
}
.action-buttons {
  margin: 0 0px 3px 0px;
  width: 1000px;
}
.status-header {
  margin-top: 8px;
}

.status-published {
  background-color: green;
  color: white;
}

.status-draft {
  background-color: orange;
  color: white;
}

.status-new {
  background-color: blue;
  color: white;
}

.status-archived {
  background-color: red;
  color: white;
}
</style>