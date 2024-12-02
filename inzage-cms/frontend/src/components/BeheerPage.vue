<template>
  <v-container>
    <v-row>
      <v-col>
        <h1>Controle gebroken links</h1>
      </v-col>
    </v-row>

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
                Kolom:
                <i>{{ getColumnLabel(linkStatus.resource, column.toString()) }}</i>
                <v-chip
                  :color="getBrokenLinksCount(links) > 0 ? 'error' : 'success'"
                  small
                  class="ma-1"
                >
                  {{ links.length - getBrokenLinksCount(links) }} / {{ links.length }}
                </v-chip>
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
              </v-expansion-panel>
            </v-expansion-panels>
            <v-alert v-else type="info" outlined> Geen links gevonden voor deze resource. </v-alert>
          </v-card-text>
        </v-card>
      </v-col>
    </v-row>
  </v-container>

  <v-snackbar v-model="snackbarError" color="error" timeout="3000">
    Er is een fout opgetreden bij het controleren van de links.
    <template #action="{ attrs }">
      <v-btn text v-bind="attrs" @click="snackbarError = false"> Sluiten </v-btn>
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
      ]
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
  },
  methods: {
    async checkLinks() {
      if (!this.selectedResource) return

      this.loading = true
      try {
        const response = await axios.get(`${store.state.APIurl}/maintainance/check_dead_links`, {
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
