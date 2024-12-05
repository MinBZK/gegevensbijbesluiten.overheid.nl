<template>
  <v-container>
    <v-row>
      <v-col>
        <h1 class="mb-5">Beheerpagina</h1>
      </v-col>
    </v-row>

    <v-expansion-panels>
      <v-expansion-panel>
        <v-expansion-panel-title> 1. Accorderingen bestanden </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row>
            <v-col cols="12">
              <v-btn
                color="primary"
                class="action-buttons"
                :loading="downloadingFiles"
                @click="downloadAllFiles"
              >
                Download alle accorderingen bestanden
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="!filesExist">
            <v-col cols="12">
              <input ref="fileInput" type="file" accept=".zip" @change="handleFileChange" />
              <v-btn
                color="primary"
                class="action-buttons"
                :loading="uploadingFiles"
                :disabled="!zipFile"
                @click="uploadAndExtract"
              >
                Uitpakken ZIP bestand en uploaden
              </v-btn>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>

      <v-expansion-panel>
        <v-expansion-panel-title> 2. Controle gebroken links </v-expansion-panel-title>
        <v-expansion-panel-text>
          <v-row>
            <v-col cols="12" md="6">
              <v-autocomplete
                v-model="selectedResource"
                :items="resources"
                item-text="title"
                item-value="resource"
                label="Selecteer een tabel"
                clearable
                hide-no-data
                @change="checkLinks"
              ></v-autocomplete>
            </v-col>
            <v-col cols="12" md="6">
              <v-btn
                color="primary"
                :loading="loading"
                :disabled="!selectedResource"
                class="action-buttons"
                @click="checkLinks"
              >
                Links controleren
              </v-btn>
            </v-col>
          </v-row>
          <v-row v-if="linkStatus">
            <v-col cols="12" md="6">
              <v-select
                v-model="linkFilter"
                :items="linkFilterOptions"
                item-title="text"
                item-value="value"
                label="Filter links"
              ></v-select>
            </v-col>
          </v-row>

          <v-row v-if="linkStatus">
            <v-col cols="12">
              <v-card elevation="1">
                <v-toolbar>
                  <v-toolbar-title>{{ getResourceLabel(linkStatus.resource) }} </v-toolbar-title>
                </v-toolbar>
                <v-card-text>
                  <v-expansion-panels v-if="hasLinks">
                    <v-expansion-panel v-for="(links, column) in filteredLinks" :key="column">
                      <v-expansion-panel-title>
                        Kolom: <i>{{ getColumnLabel(linkStatus.resource, column.toString()) }}</i>
                        <v-chip
                          :color="getBrokenLinksCount(links) > 0 ? 'error' : 'success'"
                          small
                          class="ma-1"
                        >
                          {{ links.length - getBrokenLinksCount(links) }} / {{ links.length }}
                        </v-chip>
                      </v-expansion-panel-title>
                      <v-expansion-panel-text>
                        <v-list>
                          <v-list-item
                            v-for="link in links"
                            :key="link.url"
                            :class="{ 'red lighten-4': !link.is_alive }"
                          >
                            <v-list-item-title>
                              <a :href="link.url" target="_blank" rel="noopener noreferrer">{{
                                link.url
                              }}</a>
                            </v-list-item-title>
                            <v-list-item-subtitle>
                              Code record: {{ link.primary_key }} | Beschrijving record:
                              {{ link.description }}
                            </v-list-item-subtitle>
                            <v-list-item-subtitle v-if="selectedResource">
                              <router-link
                                :to="{
                                  name: 'entityRecord',
                                  params: {
                                    id: link.primary_key,
                                    recordResource: selectedResource,
                                    resource: selectedResource,
                                    tab: 'data'
                                  },
                                  query: {
                                    redirect: $route.fullPath
                                  }
                                }"
                              >
                                Ga naar desbetreffende record
                              </router-link>
                            </v-list-item-subtitle>
                            <v-list-item-action>
                              <v-icon :color="link.is_alive ? 'success' : 'error'">
                                {{ link.is_alive ? 'mdi-check-circle' : 'mdi-alert-circle' }}
                              </v-icon>
                            </v-list-item-action>
                          </v-list-item>
                        </v-list>
                      </v-expansion-panel-text>
                    </v-expansion-panel>
                  </v-expansion-panels>
                  <v-alert v-else type="info" outlined>
                    Geen links gevonden voor deze resource.
                  </v-alert>
                </v-card-text>
              </v-card>
            </v-col>
          </v-row>
        </v-expansion-panel-text>
      </v-expansion-panel>
    </v-expansion-panels>
  </v-container>

  <v-snackbar v-model="snackbarError" color="error" timeout="3000">
    Er is een fout opgetreden bij het controleren van de links.
    <template #action="{ attrs }">
      <v-btn text v-bind="attrs" @click="snackbarError = false"> Sluiten </v-btn>
    </template>
  </v-snackbar>

  <v-snackbar v-model="snackbarSuccess" color="success" timeout="3000">
    {{ snackbarSuccessMessage }}
    <template #action="{ attrs }">
      <v-btn text v-bind="attrs" @click="snackbarSuccess = false"> Sluiten </v-btn>
    </template>
  </v-snackbar>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import { mapState } from 'vuex'
import axios from 'axios'
import store from '@/store/index'
import { tables } from '@/config/tables'
import { LinkStatus, ResourceLinkStatus } from '@/types/TableResource'

export default defineComponent({
  name: 'BeheerPage',
  data() {
    return {
      resources: tables
        .filter((table) => table.visible && table.resource !== '')
        .map((table) => ({
          title: table.label,
          resource: table.resource
        })),
      loading: false,
      snackbarError: false,
      linkFilter: 'all',
      linkFilterOptions: [
        { text: 'Alle links', value: 'all' },
        { text: 'Gebroken links', value: 'broken' },
        { text: 'Actieve links', value: 'active' }
      ],
      downloadingFiles: false,
      uploadingFiles: false,
      zipFile: null as File | null,
      snackbarSuccess: false,
      snackbarSuccessMessage: '',
      filesExist: false
    }
  },
  computed: {
    ...mapState(['linkStatus']),
    selectedResource: {
      get(): string | null {
        return store.state.selectedResource
      },
      set(value: string | null) {
        store.commit('setSelectedResource', value)
      }
    },
    hasLinks(): boolean {
      const linkStatus = this.linkStatus as ResourceLinkStatus | null
      if (!linkStatus || !linkStatus.links) return false
      return linkStatus.links && Object.values(linkStatus.links).some((links) => links.length > 0)
    },
    filteredLinks(): Record<string, LinkStatus[]> {
      if (!this.linkStatus || !this.linkStatus.links) return {}

      const filteredLinks: Record<string, LinkStatus[]> = {}
      for (const [column, links] of Object.entries(this.linkStatus.links)) {
        switch (this.linkFilter) {
          case 'broken':
            filteredLinks[column] = (links as LinkStatus[]).filter((link) => !link.is_alive)
            break
          case 'active':
            filteredLinks[column] = (links as LinkStatus[]).filter((link) => link.is_alive)
            break
          default:
            filteredLinks[column] = links as LinkStatus[]
        }
        // Remove empty arrays
        if (filteredLinks[column].length === 0) {
          delete filteredLinks[column]
        }
      }
      return filteredLinks
    }
  },
  mounted() {
    if (this.selectedResource && !this.linkStatus) {
      this.checkLinks()
    }
    this.checkFiles()
  },
  methods: {
    async checkFiles() {
      try {
        const response = await axios.get(`${store.state.APIurl}/evtp-acc/check-files/`)
        this.filesExist = response.data
      } catch (error) {
        console.error('Fout bij het controleren van bestanden:', error)
        this.filesExist = false
      }
    },
    async checkLinks() {
      if (!this.selectedResource) return

      this.loading = true
      try {
        const response = await axios.get(`${store.state.APIurl}/maintainance/check-dead-links`, {
          params: { resource: this.selectedResource }
        })
        store.commit('setLinkStatus', response.data)
      } catch (error) {
        console.error('Fout bij het controleren van links:', error)
        this.snackbarError = true
      } finally {
        this.loading = false
      }
    },
    hasBrokenLinks(links: LinkStatus[]) {
      return links.some((link) => !link.is_alive)
    },
    getResourceLabel(resource: string): string {
      const table = tables.find((t) => t.resource === resource)
      return table ? table.label : resource
    },
    getColumnLabel(resource: string, column: string): string {
      const table = tables.find((t) => t.resource === resource)
      return table && table.columns[column] ? table.columns[column] : column
    },
    getBrokenLinksCount(links: LinkStatus[]): number {
      return links.filter((link) => !link.is_alive).length
    },
    handleFileChange(event: Event) {
      const target = event.target as HTMLInputElement
      if (target.files) {
        this.zipFile = target.files[0]
      }
    },
    async downloadAllFiles() {
      this.downloadingFiles = true
      try {
        const response = await axios.get(`${store.state.APIurl}/evtp-acc/get-all-files/`, {
          responseType: 'blob'
        })
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.setAttribute('download', 'alle_accorderingen.zip')
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        this.snackbarSuccessMessage = 'Alle bestanden zijn gedownload'
        this.snackbarSuccess = true
      } catch (error) {
        console.error('Fout bij het downloaden van bestanden:', error)
        this.snackbarError = true
      } finally {
        this.downloadingFiles = false
      }
    },
    async uploadAndExtract() {
      if (!this.zipFile) return

      this.uploadingFiles = true
      const formData = new FormData()
      formData.append('zip_file', this.zipFile)

      try {
        const response = await axios.post(
          `${store.state.APIurl}/evtp-acc/upload-and-extract/`,
          formData,
          {
            headers: {
              'Content-Type': 'multipart/form-data'
            }
          }
        )
        console.log('Server response:', response.data)
        this.snackbarSuccessMessage = 'Zip bestand is geüpload en uitgepakt'
        this.snackbarSuccess = true
        if (this.$refs.fileInput) {
          ;(this.$refs.fileInput as HTMLInputElement).value = ''
        }
        this.zipFile = null
        await this.checkFiles()
      } catch (error) {
        console.error('Fout bij het uploaden en uitpakken van het zip bestand:', error)
        if ((error as any).response) {
          console.error('Server error response:', (error as any).response.data)
        }
        this.snackbarError = true
      } finally {
        this.uploadingFiles = false
      }
    }
  }
})
</script>

<style scoped>
.action-buttons {
  margin: 0 0px 3px 0px;
  width: 100%;
}
</style>
