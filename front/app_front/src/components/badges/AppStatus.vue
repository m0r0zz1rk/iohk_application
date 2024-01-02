<template>
  <ui5-badge v-if="status === 'DRAFT'" color-scheme="5">Черновик</ui5-badge>
  <ui5-badge v-if="status === 'CREATED'" color-scheme="7">Сохранена</ui5-badge>
  <ui5-badge v-if="status === 'SHIPPED'" color-scheme="1">Отправлена</ui5-badge>
  <ui5-badge v-if="status === 'ACCEPTED'" color-scheme="8">Принята</ui5-badge>
  <ui5-badge v-if="status === 'REJECTED'" color-scheme="3">Отклонена</ui5-badge>
  <ui5-badge v-if="status === 'REVOKED'" color-scheme="10">Отозвана</ui5-badge>
</template>

<script>
export default {
  name: 'AppStatus',
  props: {
    status: {type: String}
  }
}

</script>

<style scoped>

</style>