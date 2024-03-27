<template>
  <ui5-badge v-if="status === 'CREATED'" color-scheme="7">Создано</ui5-badge>
  <ui5-badge v-if="status === 'PUBLISHED'" color-scheme="8">Опубликовано</ui5-badge>
  <ui5-badge v-if="status === 'ONGOING'" color-scheme="1">В процессе</ui5-badge>
  <ui5-badge v-if="status === 'CANCELED'" color-scheme="3">Отменено</ui5-badge>
  <ui5-badge v-if="status === 'COMPLETED'" color-scheme="10">Завершено</ui5-badge>
  <ui5-badge v-if="status === 'REMOVED'" color-scheme="10">Снято с публикации</ui5-badge>
</template>

<script>
export default {
  name: 'EventStatus',
  props: {
    status: {type: String}
  }
}

</script>

<style scoped>

</style>