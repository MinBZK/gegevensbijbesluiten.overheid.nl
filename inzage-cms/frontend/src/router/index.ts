import { createWebHistory, createRouter, RouteRecordRaw } from 'vue-router'
import axios, { AxiosResponse } from 'axios'
import store from '@/store/index'
import { User } from '@/types/User'
import { tables } from '@/config/tables'
import TableCms from '@/components/TableCms.vue'
import EntityRecord from '@/components/EntityRecord.vue'
import DialogRouter from '@/components/DialogRouter.vue'

const routes: Array<RouteRecordRaw> = [
  {
    path: '/',
    name: 'Welkom',
    component: () => import('@/components/WelkomComponent.vue'),
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/logout',
    name: 'Logout',
    component: () => import('@/components/LogoutComponent.vue'),
    meta: {
      requiresAuth: false
    }
  },
  {
    path: '/:pathMatch(.*)*',
    name: 'Error',
    component: () => import('@/views/ErrorPage.vue')
  },
  {
    path: '/publiceren',
    name: 'Publiceren',
    component: () => import('@/components/Publiceren.vue'),
    meta: {
      requiresAuth: true
    }
  },
  {
    path: '/dashboard',
    name: 'DashboardCharts',
    component: () => import('@/components/DashboardCharts.vue'),
    meta: {
      requiresAuth: true
    },
    props: { tables }
  },
  {
    path: '/table/:resource',
    component: TableCms,
    name: 'table',
    meta: {
      requiresAuth: true
    },
    props: (route) => {
      return {
        resource: route.params.resource
      }
    },
    children: [
      {
        path: 'record/:recordResource/:id/:tab',
        name: 'entityRecord',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              tab: route.params.tab
            }
          }
        }
      },
      {
        path: 'new-record/:recordResource',
        name: 'newEntityRecord',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'gst-record/:recordResource/:id/:tab/:versieNr',
        name: 'entityGstRecord',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              versieNr: route.params.versieNr,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-version/:recordResource/:id/:versieNr',
        name: 'newEvtpVersion',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              versieNr: route.params.versieNr,
              tab: 'new-version-data'
            }
          }
        }
      },
      {
        path: 'duplicate-evtp-version/:recordResource/:id',
        name: 'duplicateEvtpVersion',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              tab: 'duplicate-evtp-data'
            }
          }
        }
      },
      {
        path: 'adjust-version/:recordResource/:id/:versieNr',
        name: 'adjustEvtpVersion',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              versieNr: route.params.versieNr,
              tab: 'adjust-version-data'
            }
          }
        }
      },
      {
        path: 'record/:recordResource/:id/:tab',
        name: 'entityRecordRelations',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              tab: route.params.tab
            }
          }
        }
      },
      {
        path: 'record/:recordResource/:id/:tab/:versieNr',
        name: 'entityEvtpStructure',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              resource: route.params.recordResource,
              id: route.params.id,
              tab: route.params.tab,
              versieNr: route.params.versieNr
            }
          }
        }
      },
      {
        path: 'new-gst-with-relation/:recordResource/:evtpCd/:versieNr',
        name: 'newEntityGstWithRelation',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              evtpCd: route.params.evtpCd,
              versieNr: route.params.versieNr,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-evtp-ond-with-relation/:recordResource/:evtpCd/:versieNr',
        name: 'newEntityEvtpOndWithRelation',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              evtpCd: route.params.evtpCd,
              versieNr: route.params.versieNr,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-evtp-oe-com-type-relation/:recordResource/:evtpCd/:versieNr',
        name: 'newEntityEvtpOeComTypeWithRelation',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              evtpCd: route.params.evtpCd,
              versieNr: route.params.versieNr,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },

      {
        path: 'new-gst-gg-with-relation/:recordResource/:gstCd/:versieNr',
        name: 'newEntityGstGgWithRelation',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              gstCd: route.params.gstCd,
              versieNr: route.params.versieNr,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-gst-rge-with-relation/:recordResource/:gstCd/:versieNr',
        name: 'newEntityGstRgeWithRelation',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              gstCd: route.params.gstCd,
              versieNr: route.params.versieNr,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-gst-gstt-with-relation/:recordResource/:gstCd/:versieNr',
        name: 'newEntityGstGsttWithRelation',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              gstCd: route.params.gstCd,
              versieNr: route.params.versieNr,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-gg-struct-with-relation/:recordResource/:structRelation/:structCd/',
        name: 'newEntityGGStruct',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              structCd: route.params.structCd,
              structRelation: route.params.structRelation,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-oe-koepel-with-relation/:recordResource/:structRelation/:structCd/',
        name: 'newEntityOeKoepel',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              structCd: route.params.structCd,
              structRelation: route.params.structRelation,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      },
      {
        path: 'new-oe-koepel-oe-with-relation/:recordResource/:structRelation/:structCd/',
        name: 'newEntityOeKoepelOe',
        component: DialogRouter,
        props: (route) => {
          const table = tables.find((t) => t.resource == route.params.recordResource)
          return {
            component: EntityRecord,
            title: table ? table.label : 'Record',
            maxWidthDialog: table?.maxWidthDialog,
            childProps: {
              structCd: route.params.structCd,
              structRelation: route.params.structRelation,
              resource: route.params.recordResource,
              tab: 'data'
            }
          }
        }
      }
    ]
  }
]

const router = createRouter({
  history: createWebHistory(process.env.BASE_URL),
  routes
})

const isAuthEnabled = process.env.VUE_APP_USE_AUTH === 'true'

router.beforeEach(async (to, _from, next) => {
  if (isAuthEnabled) {
    await RouterFunctions.runVerification()
    const requireAuth = to.matched.some((record) => record.meta.requiresAuth)

    // Authentication is enabled
    if (store.state.keycloak.authenticated && to.path == '/') {
      // Default if already authenticated
      next({
        path: '/dashboard',
      })
    }

    if (requireAuth) {
      if (store.state.keycloak.authenticated) {
        next()
      } else {
        next({
          path: '/',
          params: { nextUrl: to.fullPath },
        })
      }
    } else {
      next()
    }
  } else {
    // Authentication is disabled
    next()
  }
})

export const RouterFunctions = {
  runVerification: async (): Promise<AxiosResponse> => {
    return await axios
      .get(`${store.state.APIurl}/config/login/verifieer`)
      .then((response) => {
        const response_data: User = response.data
        store.commit('changeUserEmail', response_data.email)
        store.commit('changeUserAuthenticated', true)
        return response
      })
      .catch((error) => {
        store.commit('changeUserToken', '')
        store.commit('changeUserEmail', '')
        store.commit('changeUserAuthenticated', false)
        if (store.state.keycloak.authenticated) {
          store.state.keycloak.logout()
        }
        return error
      })
  }
}

export default router
