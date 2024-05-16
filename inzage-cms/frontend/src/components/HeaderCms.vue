<template>
  <div id="header-component">
    <v-app-bar
      flat
      height="125"
    >
      <v-col
        justify="center"
        align="center"
      >
        <div class="logo">
          <div class="wrapper">
            <a href="/dashboard">
              <img
                alt="Rijksoverheid Logo"
                :src="require('@/assets/logo-ro.svg')"
              >
            </a>
          </div>
        </div>
      </v-col>
    </v-app-bar>
    <v-app-bar
      :color="colour"
      flat
      height="70"
    >
      <v-toolbar-title>
        <router-link
          :to="{ name: 'DashboardCharts' }"
          style="color: #ffffff"
        >
          Beheermodule Algemene Inzage
        </router-link>
      </v-toolbar-title>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer" />
    </v-app-bar>
    <v-navigation-drawer
      v-if="getAuthentication()"
      v-model="drawer"
      location="right"
      width="350"
    >
      <v-list>
        <v-list-item
          :is="item.enabled && !item.current ? 'router-link' : 'span'"
          v-for="(item, i) in menuButtons"
          :key="i"
          :to="item.to"
        >
          <v-list-item-title
            :class="item.enabled
              ? item.current
                ? 'current-page'
                : ''
              : 'disabled-item'
            "
          >
            <router-link
              class="menu-item"
              :to="item.to"
            >
              {{ item.text }}
            </router-link>
          </v-list-item-title>
        </v-list-item>
      </v-list>
      <v-list>
        <div
          v-for="(groupData, group) in sortedTables"
          :key="group"
        >
          <span v-if="group === 'Overig'">
            <v-list-item><strong>{{ group }}</strong></v-list-item>
          </span>
          <router-link
            v-else
            class="menu-item"
            :to="{ name: 'table', params: { resource: groupData.resource } }"
          >
            <v-list-item>
              <span :class="{ 'active-link': $route.name === 'table' && $route.params.resource === groupData.resource }">
                <strong>{{ group }}</strong>
              </span>
            </v-list-item>
          </router-link>
          <v-divider />
          <v-list-item
            v-for="t in groupData.tables.filter((table) => table.resource !== groupData.resource && group !== groupData.label)"
            :key="t.label"
          >
            <router-link
              class="menu-item"
              :to="{ name: 'table', params: { resource: t.resource } }"
              active-class="active-link"
            >
              {{ t.label }}
            </router-link>
          </v-list-item>
        </div>
      </v-list>
    </v-navigation-drawer>
  </div>
</template>

<script lang="ts">
import { tables } from '@/config/tables'
import { Table } from '@/types/Tables'
import { defineComponent } from 'vue'
import store from '@/store/index'
import { getEnvironment } from '@/util/misc'
import axios from 'axios'

export default defineComponent({
  name: 'HEADER',
  data() {
    return {
      drawer: false as boolean,
      tables,
      envObj: [] as Array<object>,
      colour: '' as string,
      environment: '' as string,
    }
  },
  computed: {
    sortedTables() {
      const groupedTables = tables
        .reduce((acc, table) => {
          const group = table.group || 'Overig'
          if (!acc[group]) {
            acc[group] = []
          }
          acc[group].push(table)
          return acc
        }, {} as { [key: string]: Table[] })

      const sortedGroupedTables = Object.entries(groupedTables).reduce(
        (acc, [group, tables]) => {
          const resource = tables[0].resource
          acc[group] = {
            group,
            resource,
            tables: tables.sort((a, b) =>
              a.label.localeCompare(b.label, undefined, { numeric: true })
            ),
          }
          return acc
        },
        {} as { [key: string]: { group: string; resource: string; tables: Table[] } }
      )
      return sortedGroupedTables
    },
    menuButtons(): {
      text: string
      to: string
      enabled: boolean
      current: boolean
    }[] {
      return [
        {
          text: 'Dashboard',
          to: '/dashboard',
          enabled: store.state.user.isAuthenticated,
          current: this.$route.name == 'dashboard',
        },
        {
          text: 'Publiceren',
          to: '/publiceren',
          enabled: store.state.user.isAuthenticated,
          current: this.$route.name == 'Publiceren',
        },
        {
          text: 'Uitloggen',
          to: '/logout',
          enabled: store.state.user.isAuthenticated,
          current: this.$route.name == 'Logout',
        },
      ]
    },
  },
  watch: {
    group() {
      this.drawer = false
    },
  },
  async created() {
    try {
      const { data } = await axios.get(`${store.state.APIurl}/config/pod-env`)
      this.envObj = data
      this.environment = getEnvironment(this.envObj, 'ENVIRONMENT')
      this.getColour(this.environment)
    } catch (e) {
      console.error(e)
    }
  },
  methods: {
    getColour(environment: string) {
      if (environment === 'productie') {
        this.colour = 'primary'
      } else if (environment === 'acceptatie') {
        this.colour = 'green'
      } else if (environment === 'test') {
        this.colour = 'orange'
      } else {
        this.colour = 'primary'
      }
    },
    getAuthentication() {
      const isAuthEnabled = process.env.VUE_APP_USE_AUTH === 'true'
      if (!isAuthEnabled) {
        return true
      }
      return store.state.user.isAuthenticated
    },
  },
})
</script>

<style scoped>
.active-link {
  background-color: #bedef0;
  border: 2px dotted #444;
}
.wrapper {
  display: flex;
  flex-basis: 100%;
  flex-wrap: wrap;
  max-width: 1200px;
  align-items: flex-start;
  margin-right: 130px;
  justify-content: center;
}

.logo .wrapper img {
  width: inherit;
  max-width: 1168px;
  transform: translateX(50%);
}

.v-toolbar__content>.v-btn {
  align-self: center !important;
  margin-right: 40px !important;
  font-size: 26px;
  text-transform: capitalize !important;
}

.v-toolbar__content .v-btn.v-btn--icon.v-size--default {
  height: 48px;
  width: 120px !important;
}

.v-toolbar-title {
  align-self: center !important;
  font-size: 26px;
  margin-left: 50px;
  color: azure;
}

.mdi-menu {
  margin-right: 8px !important;
}

.menu-item {
  text-decoration: none !important;
}

.current-page {
  background-color: lightgray;
}

.disabled-item {
  color: lightgray;
}

.v-list-item {
  min-height: 36px;
  padding: 0;
}

.v-list-item__title {
  padding: 8px 12px;
}
</style>
