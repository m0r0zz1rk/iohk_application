<template>
  <Editor v-if="(editorText.length > 0) && (full)"
      v-model="editorText"
      :api-key="TinyMCEAPIKey"
      :init="{
         height: editorHeight,
         menubar: 'edit table',
         language: 'ru',
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | bold italic underline strikethrough | \
           fontselect fontsizeselect formatselect | \
           alignleft aligncenter alignright alignjustify | \
           outdent indent |  numlist bullist checklist | \
           forecolor backcolor casechange permanentpen formatpainter removeformat | \
           pagebreak | charmap emoticons | preview save | \
           insertfile image pageembed template link codesample | \
           a11ycheck ltr rtl',
         images_upload_handler: (blobInfo, success, failure) => {
            imagesUploadHandler(blobInfo, success, failure)
         }
      }"
  />
  <Editor v-if="!(full)"
          v-model="editorText"
          :api-key="TinyMCEAPIKey"
          :init="{
         height: editorHeight,
         menubar: 'edit table',
         language: 'ru',
         plugins: [
           'advlist autolink lists link image charmap print preview anchor',
           'searchreplace visualblocks code fullscreen',
           'insertdatetime media table paste code help wordcount'
         ],
         toolbar:
           'undo redo | bold italic underline strikethrough | \
           fontselect fontsizeselect formatselect | \
           alignleft aligncenter alignright alignjustify | \
           outdent indent |  numlist bullist checklist | \
           forecolor backcolor casechange permanentpen formatpainter removeformat | \
           pagebreak | charmap emoticons | preview save',
      }"
  />
</template>

<script>
import Editor from '@tinymce/tinymce-vue'
import {apiRequest} from "../additional/functions/api_request.js";

export default {
  name: 'TinyMCE',
  components: {Editor},
  props: {
    full: {type: Boolean},
    Information: {type: String},
    additionalData: {type: Object},
    editorHeight: {type: Number}
  },
  data() {
    return {
      editorText: '',
      TinyMCEAPIKey: import.meta.env.VITE_APP_TINYMCE_API_KEY
    }
  },
  methods: {
    init() {
      if (this.Information) {
        this.editorText = this.Information
      }
    },
    async imagesUploadHandler(blobInfo, success, failure) {
      let formRequest = new FormData()
      formRequest.append('file', blobInfo.blob(), blobInfo.filename())
      formRequest.append('name', this.additionalData['name'])
      apiRequest(
          this.$store.state.backendUrl+'/api/v1/commons/tinymce_image/',
          'PUT',
          true,
          formRequest,
          true,
          false
      )
          .then(data => {
            if (data.location) {
              success(this.$store.state.backendUrl+data.location)
            } else {
              failure(data.error)
            }
          })
    }
  },
  beforeMount() {
    this.init()
  }
}
</script>

<style scoped>

</style>