<template>
  <v-container fluid class="OverviewEvtpTree pa-0 bg-grey-lighten-2 overflow-y-hidden">
    <v-row class="header ma-0 bg-white">
      <v-col v-if="loading == false" cols="8" class="pa-4">
        <v-row>
          <v-col cols="auto" class="pb-0">
            <v-icon role="button" class="mb-1" @click="() => $emit('close')">mdi-arrow-left</v-icon>
            <span class="text-h6 ml-2">{{ `Geselecteerde besluit: ${evtpTree.evtp_nm}` }}</span>
            <v-btn
              color="primary"
              variant="outlined"
              class="mb-1"
              :disabled="disableEvtp"
              :to="{
                name: 'entityRecord',
                params: {
                  id: evtpCd,
                  recordResource: 'evtp-version',
                  tab: 'data'
                },
                query: {
                  redirect: $route.fullPath
                }
              }"
            >
              <v-icon> mdi-pencil </v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-row class="align-center mt-0">
          <v-col cols="auto"> Besluitnemende organisatie: </v-col>
          <v-col cols="auto">
            {{ evtpTree.verantwoordelijke_oe?.naam_officieel }}
          </v-col>
        </v-row>
        <v-row class="align-center mt-0">
          <v-col cols="auto">
            <router-link :to="{ name: 'table', params: { resource: 'ond' } }">
              Onderwerpen(en):
            </router-link>
          </v-col>
          <v-col class="pa-0">
            <v-chip-group>
              <v-chip
                v-for="ond in evtpTreeDirectlyRelated.ond"
                :key="ond.evtp_ond_cd"
                :index="ond.evtp_ond_cd"
                :disabled="disableEvtp"
                close
                rounded="lg"
                class="bg-primary"
              >
                {{ ond.titel }}
                <v-icon
                  v-if="!disableEvtp"
                  right
                  @click="deleteRelation('evtp-ond', ond.evtp_ond_cd)"
                  >mdi-close</v-icon
                >
              </v-chip>
              <v-btn
                color="primary"
                flat
                class="mb-1 mt-1 circle"
                :disabled="disableEvtp"
                :to="{
                  name: 'newEntityEvtpOndWithRelation',
                  params: {
                    evtpCd: evtpCd,
                    versieNr: versieNr,
                    recordResource: 'evtp-ond'
                  },
                  query: {
                    redirect: $route.fullPath
                  }
                }"
              >
                <v-icon> mdi-plus </v-icon>
              </v-btn>
            </v-chip-group>
          </v-col>
        </v-row>
        <v-row class="align-center mt-0">
          <v-col cols="auto" class="pt-0.5">
            <router-link :to="{ name: 'table', params: { resource: 'oe-com-type' } }">
              Communicatiekanaal:
            </router-link>
          </v-col>
          <v-col
            v-for="oeComType in evtpTreeDirectlyRelated.oeComType"
            :key="oeComType.oe_com_type_cd"
            style="padding: 6px"
          >
            {{ oeComType.omschrijving }}
            <v-btn
              color="primary"
              variant="outlined"
              class="mb-1"
              :disabled="disableEvtp"
              :to="{
                name: 'entityRecord',
                params: {
                  id: oeComType.evtp_oe_com_type_cd,
                  recordResource: 'evtp-oe-com-type',
                  tab: 'data'
                },
                query: {
                  redirect: $route.fullPath
                }
              }"
            >
              <v-icon> mdi-pencil </v-icon>
            </v-btn>
          </v-col>
          <v-col v-if="evtpTreeDirectlyRelated.oeComType.length == 0">
            <v-btn
              color="primary"
              class="circle"
              flat
              :disabled="disableEvtp"
              :to="{
                name: 'newEntityEvtpOeComTypeWithRelation',
                params: {
                  evtpCd: evtpCd,
                  versieNr: versieNr,
                  recordResource: 'evtp-oe-com-type'
                },
                query: {
                  redirect: $route.fullPath
                }
              }"
            >
              <v-icon> mdi-plus </v-icon>
            </v-btn>
          </v-col>
        </v-row>
        <v-row class="align-center mt-0">
          <v-col cols="auto">
            <router-link :to="{ name: 'table', params: { resource: 'omg' } }">
              Organisatie omgeving (optioneel):
            </router-link>
          </v-col>
          <v-col v-if="!evtpTreeDirectlyRelated.omg">
            <v-btn
              color="primary"
              flat
              class="mb-1 circle"
              :disabled="disableEvtp"
              :to="{
                name: 'entityRecord',
                params: {
                  id: evtpCd,
                  recordResource: 'evtp-version',
                  tab: 'data'
                },
                query: {
                  redirect: $route.fullPath
                }
              }"
            >
              <v-icon> mdi-plus </v-icon>
            </v-btn>
          </v-col>
          <v-col v-else style="padding: 6px">
            {{ evtpTreeDirectlyRelated.omg?.titel || '' }}
            <v-btn
              color="primary"
              variant="outlined"
              :disabled="disableEvtp"
              class="mb-1"
              :to="{
                name: 'entityRecord',
                params: {
                  id: evtpCd,
                  versieNr: versieNr,
                  recordResource: 'evtp-version',
                  tab: 'data'
                },
                query: {
                  redirect: $route.fullPath
                }
              }"
            >
              <v-icon> mdi-pencil </v-icon>
            </v-btn>
          </v-col>
        </v-row>
      </v-col>
      <v-col v-if="loading == false" cols="4" class="pa-4">
        <v-select
          v-model="selectedVersion"
          label="Selecteer versie"
          :items="evtpVersions"
          outlined
          dense
        ></v-select>
        <v-text-field
          v-model="selectedIdPublicatiestatus"
          label="Status publicatie"
          :bg-color="
            selectedIdPublicatiestatus === getPublicatieStatus(1)
              ? 'rgb(0, 0, 255)'
              : selectedIdPublicatiestatus === getPublicatieStatus(2)
              ? 'orange'
              : 'green'
          "
          class="noHover"
          readonly
          outlined
          dense
        ></v-text-field>
      </v-col>
      <v-alert v-if="disableEvtp && loading == false" type="info" color="green" class="pa-1">
        <strong>Let op!</strong> Dit besluit is inmiddels gepubliceerd of verouderd en kan niet meer
        worden gewijzigd.
      </v-alert>
    </v-row>
    <v-row v-if="loading == false" class="body ma-0 overflow-v-data-table">
      <v-col cols="12" class="pa-4">
        <v-data-table
          :headers="headers"
          :items="sortedTableItems"
          fixed-header
          item-key="naam"
          class="elevation-1 hyphen"
          items-per-page="-1"
        >
          <template v-for="header in headers" :key="header.value" #[`header.${header.value}`]>
            <v-row>
              <v-col class="align-to-the-middle">
                <router-link :to="{ name: 'table', params: { resource: header.resource } }">
                  {{ header.title }}
                </router-link>
              </v-col>
              <v-col v-if="header.resource == 'gst'" cols="auto">
                <v-btn
                  color="primary"
                  class="circle"
                  :disabled="disableEvtp"
                  flat
                  :to="{
                    name: 'newEntityGstWithRelation',
                    params: {
                      evtpCd: evtpCd,
                      oeBestCd: evtpTree.verantwoordelijke_oe?.oe_cd,
                      versieNr: versieNr,
                      recordResource: 'gst'
                    },
                    query: {
                      redirect: $route.fullPath
                    }
                  }"
                >
                  <v-icon> mdi-plus </v-icon>
                </v-btn>
              </v-col>
            </v-row>
          </template>
          <template #item="{ item, index }">
            <tr :class="{ 'alternate-row': index % 2 === 1 }">
              <td>
                <v-row class="align-center my-2">
                  <v-btn
                    color="white"
                    flat
                    outlined
                    class="mx-1"
                    :disabled="disableEvtp"
                    style="outline: grey solid 2px"
                    :to="{
                      name: 'entityRecord',
                      params: {
                        id: item.evtpGst.evtp_gst_cd,
                        recordResource: 'evtp-gst',
                        tab: 'data'
                      },
                      query: {
                        redirect: $route.fullPath
                      }
                    }"
                  >
                    {{ index + 1 }}
                  </v-btn>
                  <v-col class="pl-1 pr-0">
                    <v-tooltip :text="item.gst.omschrijving">
                      <template #activator="{ props }">
                        <router-link
                          v-bind="props"
                          :to="{
                            name: 'entityRecord',
                            params: {
                              id: item.gst.gst_cd,
                              recordResource: 'gst',
                              tab: 'data'
                            },
                            query: {
                              redirect: $route.fullPath
                            }
                          }"
                        >
                          {{ truncatedText(item.gst.omschrijving, 35) }}
                        </router-link>
                      </template>
                    </v-tooltip>
                    <v-tooltip :text="item.gst.conditie">
                      <template #activator="{ props }">
                        <div v-bind="props">
                          <i>{{ truncatedText(item.gst.conditie, 30) }}</i>
                        </div>
                      </template>
                    </v-tooltip>
                  </v-col>
                  <v-col cols="auto" class="pa-0">
                    <v-btn variant="outlined" class="pa-1" @click="deleteEvtpGst(item)">
                      <v-icon v-if="!disableEvtp">mdi-close</v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </td>
              <td>
                <v-row class="align-center mb-2">
                  <v-col class="pr-0">
                    <v-tooltip :text="item.oeBron">
                      <template #activator="{ props }">
                        <div v-bind="props">
                          {{ truncatedText(item.oeBron, 22) }}
                        </div>
                      </template>
                    </v-tooltip>
                    <v-tooltip :text="item.ibron">
                      <template #activator="{ props }">
                        <div v-bind="props" class="font-italic">
                          {{ truncatedText(item.ibron, 22) }}
                        </div>
                      </template>
                    </v-tooltip>
                  </v-col>
                  <v-col cols="auto" class="pa-0">
                    <v-btn
                      color="primary"
                      variant="outlined"
                      :disabled="disableEvtp"
                      :to="{
                        name: 'entityRecord',
                        params: {
                          id: item.gst.gst_cd,
                          recordResource: 'gst',
                          tab: 'data'
                        },
                        query: {
                          redirect: $route.fullPath
                        }
                      }"
                    >
                      <v-icon> mdi-pencil </v-icon>
                    </v-btn>
                  </v-col>
                </v-row>
              </td>
              <td :class="{ gegevensstroomtype: item.gstType.length == 0 }">
                <div v-if="item.gstType.length > 0">
                  <v-row
                    v-for="gstType in item.gstType"
                    :key="gstType.gst_gstt_cd"
                    class="align-center mb-2"
                  >
                    <v-col class="pr-0">
                      <v-tooltip :text="gstType.gstt_naam">
                        <template #activator="{ props }">
                          <router-link
                            v-bind="props"
                            :to="{
                              name: 'entityRecord',
                              params: {
                                id: gstType.gst_gstt_cd,
                                recordResource: 'gst-gstt',
                                tab: 'data'
                              },
                              query: {
                                redirect: $route.fullPath
                              }
                            }"
                          >
                            {{ truncatedText(gstType.gstt_naam, 30) }}
                          </router-link>
                        </template>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="auto" class="pa-0">
                      <v-btn
                        variant="outlined"
                        @click="deleteRelation('gst-gstt', gstType.gst_gstt_cd)"
                      >
                        <v-icon v-if="!disableEvtp" right>mdi-close</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                </div>
                <div v-else class="d-flex justify-space-between align-center mb-1 mt-1">
                  <i> Voeg een gegevensstroomtype toe</i>
                  <v-btn
                    color="primary"
                    class="circle"
                    :disabled="disableEvtp"
                    flat
                    :to="{
                      name: 'newEntityGstGsttWithRelation',
                      params: {
                        gstCd: item.gst.gst_cd,
                        versieNr: versieNr,
                        recordResource: 'gst-gstt'
                      },
                      query: {
                        redirect: $route.fullPath
                      }
                    }"
                  >
                    <v-icon> mdi-plus </v-icon>
                  </v-btn>
                </div>
                <v-divider v-if="item.gstType.length == 0" class="mb-2"></v-divider>
              </td>
              <td class="gegevensgroepen">
                <div class="d-flex justify-space-between align-center mb-1 mt-1">
                  <v-tooltip v-if="item.ggParent" :text="item.ggParent.omschrijving">
                    <template #activator="{ props }">
                      <strong v-bind="props">{{
                        truncatedText(item.ggParent.omschrijving)
                      }}</strong>
                    </template>
                  </v-tooltip>
                  <i v-else> Voeg een gegevensgroep toe</i>
                  <v-btn
                    v-if="!item.ggParent"
                    color="primary"
                    class="circle"
                    flat
                    :disabled="disableEvtp"
                    :to="{
                      name: 'newEntityGstGgWithRelation',
                      params: {
                        gstCd: item.gst.gst_cd,
                        versieNr: versieNr,
                        recordResource: 'gst-gg'
                      },
                      query: {
                        redirect: $route.fullPath
                      }
                    }"
                  >
                    <v-icon small>mdi-plus</v-icon>
                  </v-btn>
                  <v-btn
                    v-if="item.ggParent"
                    color="primary"
                    class="circle"
                    flat
                    :disabled="disableEvtp"
                    :to="{
                      name: 'newEntityGstGgWithRelationFiltered',
                      params: {
                        gstCd: item.gst.gst_cd,
                        ggCdParent: item.ggParent.gg_cd,
                        versieNr: versieNr,
                        recordResource: 'gst-gg'
                      },
                      query: {
                        redirect: $route.fullPath
                      }
                    }"
                  >
                    <v-icon small>mdi-plus</v-icon>
                  </v-btn>
                </div>
                <v-divider class="mb-2"></v-divider>
                <template v-for="(ggChild, indexGgChild) in item.ggChild" :key="indexGgChild">
                  <v-row class="align-center">
                    <v-col class="pr-0">
                      <v-btn
                        color="white"
                        flat
                        outlined
                        class="ma-1"
                        :disabled="disableEvtp"
                        style="outline: grey solid 2px"
                        :to="{
                          name: 'entityRecord',
                          params: {
                            id: ggChild.gst_gg_cd,
                            recordResource: 'gst-gg',
                            tab: 'data'
                          },
                          query: {
                            redirect: $route.fullPath
                          }
                        }"
                      >
                        {{ indexGgChild + 1 }}
                      </v-btn>
                      <v-tooltip :text="ggChild.omschrijving">
                        <template #activator="{ props }">
                          <span v-bind="props" class="pl-1">
                            {{ truncatedText(ggChild.omschrijving, 38) }}
                          </span>
                        </template>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="auto" class="pl-0">
                      <v-btn
                        variant="outlined"
                        class="pa-1"
                        @click="deleteRelation('gst-gg', ggChild.gst_gg_cd)"
                      >
                        <v-icon v-if="!disableEvtp">mdi-close</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                  <v-divider></v-divider>
                </template>
              </td>
              <td class="regelingen">
                <div class="d-flex justify-space-between align-center mb-1 mt-1">
                  <i v-if="item.rge.length == 0"> Voeg een wettelijke regeling toe</i>
                  <span v-else></span>
                  <v-btn
                    color="primary"
                    class="circle"
                    :disabled="disableEvtp"
                    flat
                    :to="{
                      name: 'newEntityGstRgeWithRelation',
                      params: {
                        gstCd: item.gst.gst_cd,
                        versieNr: versieNr,
                        recordResource: 'gst-rge'
                      },
                      query: {
                        redirect: $route.fullPath
                      }
                    }"
                  >
                    <v-icon small>mdi-plus</v-icon>
                  </v-btn>
                </div>
                <v-divider class="mb-2"></v-divider>
                <template v-for="(rge, indexRge) in item.rge" :key="indexRge">
                  <v-row v-if="item.rge.length > 0" class="align-center">
                    <v-col class="pr-0">
                      <v-btn
                        color="white"
                        flat
                        outlined
                        class="ma-1"
                        :disabled="disableEvtp"
                        style="outline: grey solid 2px"
                        :to="{
                          name: 'entityRecord',
                          params: {
                            id: rge.gst_rge_cd,
                            recordResource: 'gst-rge',
                            tab: 'data'
                          },
                          query: {
                            redirect: $route.fullPath
                          }
                        }"
                      >
                        {{ indexRge + 1 }}
                      </v-btn>
                      <v-tooltip :text="rge.titel">
                        <template #activator="{ props }">
                          <span v-bind="props" class="pl-1">
                            {{ truncatedText(rge.titel, 18) }}
                          </span>
                        </template>
                      </v-tooltip>
                    </v-col>
                    <v-col cols="auto" class="pl-0">
                      <v-btn
                        variant="outlined"
                        class="pa-1"
                        @click="deleteRelation('gst-rge', rge.gst_rge_cd)"
                      >
                        <v-icon v-if="!disableEvtp" right>mdi-close</v-icon>
                      </v-btn>
                    </v-col>
                  </v-row>
                  <v-divider class="mb-2"></v-divider>
                </template>
              </td>
            </tr>
          </template>
          <template #bottom></template>
          <template #no-data>
            <i v-if="!disableEvtp"> Voeg een gegevensstroom toe </i>
          </template>
        </v-data-table>
      </v-col>
    </v-row>
    <v-row v-else class="justify-center align-center">
      <v-progress-circular indeterminate color="primary" class="mr-2" />
      <span>Ophalen van alle relaties...</span>
    </v-row>
  </v-container>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import axios from 'axios'
import store from '@/store/index'
import {
  gstGstType,
  ond,
  oeComType,
  gst,
  oeBron,
  ggChild,
  rge,
  ggParent,
  omg,
  ibron,
  evtpGst
} from '@/util/flatEvtpTree'
import type { OndTree } from '@/types/Ond'
import type { OeComTypeTree } from '@/types/Oe'
import type { Omg, EvtpTree, EntityInDirectlyRelated } from '@/types/EvtpVersion'
import { getPublicatieStatus } from '@/types/PublicatieStatus'

export default defineComponent({
  name: 'OverviewEvtpTree',
  props: {
    evtpCd: {
      type: [String, Number],
      required: true
    },
    versieNr: {
      type: [Number, String],
      default: null,
      required: true
    },
    resource: {
      type: String,
      required: true
    },
    title: {
      type: String,
      default: null
    }
  },
  emits: ['relationUpdated', 'close'],
  data() {
    return {
      headers: [
        { title: 'Gegevenstromen', value: 'gegevenstromen', width: '13em', resource: 'gst' },
        { title: 'Organisaties', value: 'organisaties', width: '9em', resource: 'oe' },
        { title: 'Gegevensstroomtype', value: 'type', width: '10em', resource: 'gst-type' },
        { title: 'Gegevensgroepen', value: 'gegevensgroepen', width: '15em', resource: 'gg' },
        { title: 'Wettelijke regelingen', value: 'regelingen', width: '10em', resource: 'rge' }
      ] as const,
      selectedIdPublicatiestatus: '' as string,
      loading: true as boolean,
      selectedVersion: this.versieNr as number,
      evtpTree: {} as EvtpTree,
      evtpVersions: [] as Array<number>
    }
  },
  computed: {
    evtpTreeDirectlyRelated() {
      interface EntityTreeDirectlyRelated {
        ond: OndTree[]
        oeComType: OeComTypeTree[]
        omg: Omg | ''
      }

      const relations: EntityTreeDirectlyRelated = {
        ond: ond(this.evtpTree),
        oeComType: oeComType(this.evtpTree),
        omg: omg(this.evtpTree)
      }

      return relations
    },
    evtpTreeIndirectlyRelated() {
      const relations: EntityInDirectlyRelated = {
        evtpGst: evtpGst(this.evtpTree),
        gst: gst(this.evtpTree),
        gstType: gstGstType(this.evtpTree),
        ibron: ibron(this.evtpTree),
        oeBron: oeBron(this.evtpTree),
        ggChild: ggChild(this.evtpTree),
        ggParent: ggParent(this.evtpTree),
        rge: rge(this.evtpTree)
      }

      return relations
    },
    disableEvtp() {
      return this.evtpTree.id_publicatiestatus == 3 || this.evtpTree.versie_nr < this.versieNr
    },
    tableItems() {
      const relations = this.evtpTreeIndirectlyRelated

      return relations.gst.map((gstItem, index) => {
        const ggParent = relations.ggParent[index]
        return {
          evtpGst: relations.evtpGst[index],
          gst: gstItem,
          gstType: relations.gstType[index],
          ibron: relations.ibron[index]?.titel,
          oeBron: relations.oeBron[index]?.naam_officieel,
          ggChild: relations.ggChild[index],
          ggParent: ggParent[0],
          rge: relations.rge[index]
        }
      })
    },
    sortedTableItems() {
      return [...this.tableItems].sort((a, b) => {
        const sortKeyA = a.evtpGst.sort_key
        const sortKeyB = b.evtpGst.sort_key
        return sortKeyA - sortKeyB
      })
    }
  },
  watch: {
    async selectedVersion() {
      await this.fetchData()
    }
  },
  async mounted() {
    await this.fetchData()
  },
  methods: {
    getPublicatieStatus(statusId: number) {
      return getPublicatieStatus(statusId)
    },
    truncatedText(text: string, cutoff = 40) {
      return text ? (text.length > cutoff ? text.substring(0, cutoff) + '...' : text) : text
    },
    getEntityRecordHref(id: number, resource: string) {
      return (
        this?.$router?.resolve({
          name: 'entityRecord',
          params: {
            id,
            resource,
            recordResource: resource,
            tab: 'data'
          },
          query: {
            redirect: this.$route?.fullPath
          }
        })?.href || ''
      )
    },
    async fetchData() {
      const { data: relationsData } = await axios.get(
        `${store.state.APIurl}/${this.resource}/relations/${this.evtpCd}/${this.selectedVersion}`
      )
      this.evtpTree = relationsData
      this.selectedIdPublicatiestatus = getPublicatieStatus(this.evtpTree.id_publicatiestatus)
      const { data: versionsData } = await axios.get(
        `${store.state.APIurl}/${this.resource}-versions/${this.evtpCd}`
      )
      this.evtpVersions = versionsData.map((version: number) => version)
      this.loading = false
    },
    async deleteRelation(resource: string, id: number) {
      await axios.delete(`${store.state.APIurl}/${resource}/${id}`)
      await this.fetchData()
    },
    async deleteEvtpGst(item) {
      // 1. Delete gst_gg
      const postPromisesGstGg = await Promise.all(
        item.ggChild.map((gg) => {
          return axios.delete(`${store.state.APIurl}/gst-gg/${gg.gst_gg_cd}`)
        })
      )

      // 2. Delete evtp_gst
      const postPromisesEvtpGst = await axios.delete(
        `${store.state.APIurl}/evtp-gst/${item.evtpGst.evtp_gst_cd}`
      )

      // 3. Delete gst_gstt
      const postPromisesGstGstt = await Promise.all(
        item.gstType.map((gst_gstt) => {
          return axios.delete(`${store.state.APIurl}/gst-gstt/${gst_gstt.gst_gstt_cd}`)
        })
      )

      // 4. Delete gst_rge
      const postPromisesGstRge = await Promise.all(
        item.rge.map((gst_rge) => {
          return axios.delete(`${store.state.APIurl}/gst-rge/${gst_rge.gst_rge_cd}`)
        })
      )

      const postPromise = [
        postPromisesEvtpGst,
        postPromisesGstGg,
        postPromisesGstGstt,
        postPromisesGstRge
      ]
      Promise.all(postPromise).then(() => {
        this.fetchData()
      })
    }
  }
})
</script>

<style scoped>
.OverviewEvtpTree {
  height: 150vh;
  background-color: #e7f2fa;
  overflow-x: hidden;
}

.v-data-table >>> table {
  table-layout: fixed;
}

.font-italic {
  font-style: italic;
}

.v-data-table >>> tbody tr:nth-child(even) {
  background-color: #e3f2fd !important;
}

.v-data-table >>> th,
.v-data-table >>> td {
  border-right: 1.5px solid #ddd;
  border-top: 1.5px solid #ddd;
}

.hyphen {
  hyphens: auto;
  word-break: break-word;
}

.gegevensgroepen,
.gegevensstroomtype,
.regelingen {
  vertical-align: top;
}

.gegevensgroepen > div,
.regelingen > div {
  min-height: 1.5em;
}

.v-divider {
  margin-top: 0.5em;
  margin-bottom: 0.5em;
}

.v-btn {
  min-width: 32px;
  width: 32px;
  height: 32px;
  border-color: rgba(0, 0, 0, 0);
}

.gegevensgroepen > div:empty,
.regelingen > div:empty {
  min-height: 1.5em;
}
.align-to-the-middle {
  display: flex;
  align-items: center;
}
.overflow-v-data-table {
  overflow-y: auto;
  max-height: calc(100vh - 295px);
}
.noHover {
  pointer-events: none;
}
.circle {
  border-radius: 20px !important;
}
</style>
