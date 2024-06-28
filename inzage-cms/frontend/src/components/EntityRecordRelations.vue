<template>
  <v-card-text class="form-container">
    <v-timeline side="end">
      <template
        v-for="(relation, index) in relations"
        :key="relation.label"
      >
        <v-timeline-item
          :dot-color="relation.color"
          size="small"
        >
          <strong>{{ relation.label }}</strong>
          <v-card-text>
            <EntityRecordRelationsTable
              :relation-values="relation.values"
              :primary-key="primaryKey"
              :description-key="descriptionKey"
              :relation-label="relation.label"
              :relation-key="relation.relationKey"
              :resource="getForeignTable(relation.relationKey).resource"
              :record-id="record[primaryKey]"
              :endpoint="getEndpoint(relation.relationKey)"
              :is-koepel="isKoepel"
              @relation-updated="$emit('relationUpdated')"
            />
          </v-card-text>
        </v-timeline-item>
        <v-timeline-item
          v-if="index == 0"
          dot-color="primary"
          size="small"
        >
          <strong>Geselecteerde entiteit</strong>
          <v-card-text>{{ record[descriptionKey] }}</v-card-text>
        </v-timeline-item>
      </template>
    </v-timeline>
  </v-card-text>
  <v-card-actions>
    <v-spacer />
    <v-btn
      color="primary"
      @click="$emit('close')"
    >
      Scherm afsluiten
    </v-btn>
  </v-card-actions>
</template>

<script lang="ts">
import { defineComponent } from 'vue'
import store from '@/store/index'
import EntityRecordRelationsTable from '@/components/EntityRecordRelationsTable.vue'

export default defineComponent({
  name: 'EntityRecordRelations',
  components: { EntityRecordRelationsTable },
  props: {
    record: {
      type: Object,
      default: () => { },
    },
    primaryKey: {
      type: String,
      required: true,
    },
    foreignKeys: {
      type: Object,
      required: true,
    },
    descriptionKey: {
      type: String,
      required: true,
    },
    resource: {
      type: String,
      required: true,
    },
  },
  emits: ['close', 'relationUpdated'],
  data() {
    return {
      self: {} as object,
    }
  },
  computed: {
    children() {
      return this.record.child_entities
        ? this.record.child_entities.map((entity) => {
          entity.relatedEntity = entity.child_entity
          return entity
        })
        : []
    },
    parents() {
      return this.record.parent_entities
        ? this.record.parent_entities.map((entity) => {
          entity.relatedEntity = entity.parent_entity
          return entity
        })
        : []
    },
    relations() {
      interface Entity {
        values: Array<object>
        label: string
        color: string
        relationKey: string

      }

      const relations: Array<Entity> = [
        {
          values: this.resource.endsWith('koepel') ? this.children : this.parents,
          label: this.resource.endsWith('koepel') ? 'Onderliggende entiteiten' : 'Bovenliggende entiteit',
          color: 'secondary',
          relationKey: this.resource.endsWith('koepel') ? 'children' : 'parents',
        },
      ]
      return relations
    },
    isKoepel() {
      return this.resource.endsWith('koepel')
    }
  },
  methods: {
    getForeignKey(relationKey) {
      const relationFieldMapping = {
        parents: 'parent_entities',
        children: 'child_entities',
      }
      const foreignKey = this.foreignKeys.find(
        (fK) => fK['foreign_key'] == relationFieldMapping[relationKey]
      )
      return foreignKey
    },
    getForeignTable(relationKey) {
      return this.getForeignKey(relationKey).foreign_table
    },
    getEndpoint(relationKey) {
      const foreignKey = this.getForeignKey(relationKey)
      return `${store.state.APIurl}/${foreignKey.foreign_table.resource}`
    },
  },
})
</script>
