<template>
  <div
    id="statusbar"
    class="px-0 px-lg-5 pl-2"
    style="min-height: 3.6rem;"
  >
    <b-container
      fluid
      class="px-0"
    >
      <b-navbar
        toggleable="lg"
        type="light"
        variant=""
      >
        <div class="separator" />
        <div class="d-flex flex-grow">
          <!-- Left aligned nav items-->
          <b-navbar-nav
            id="statusbar-content"
            class="flex-grow flex-row"
          >
            <!-- Back to deployments -->
            <b-nav-item
              v-if="checkLocation('deployment_desktops')"
              href="#"
              @click="goToDeployments"
            >
              <VisibilityModal />
              <div>
                <b-icon
                  icon="arrow-left"
                  aria-hidden="true"
                  class="text-medium-gray mr-2 mr-lg-2"
                />
                {{ $t("components.statusbar.deployment.back") }}
              </div>
            </b-nav-item>
            <!-- Back to deployment desktop list -->
            <b-nav-item
              v-if="checkLocation('deployment_videowall')"
              href="#"
              @click="redirectDeployment"
            >
              <div>
                <b-icon
                  icon="arrow-left"
                  aria-hidden="true"
                  class="text-medium-gray mr-2 mr-lg-2"
                />
                {{ $t("components.statusbar.videowall.back") }}
              </div>
            </b-nav-item>
            <!-- filter -->
            <DesktopsFilter
              v-if="(checkLocation('desktops') || checkLocation('deployment_videowall')) && !creationMode"
              class="d-none d-lg-flex"
            />
            <!-- Only started checkbox -->
            <b-nav-item
              v-if="(checkLocation('desktops') || checkLocation('deployment_videowall')) && !creationMode"
              class="ml-2 ml-md-4"
              href="#"
              @click="startedFilter"
            >
              <div>
                <b-form-checkbox
                  id="started-checkbox"
                  v-model="started"
                  name="checkbox-1"
                  value="true"
                  unchecked-value="false"
                  aria-hidden="true"
                  class="mr-2 mr-lg-0"
                >
                  <p class="d-none d-md-inline p-0 m-0">
                    {{ $t("components.statusbar.checkbox-text") }}
                  </p>
                  <p class="d-inline d-md-none  p-0 m-0">
                    {{ $t("components.statusbar.checkbox-text-short") }}
                  </p>
                </b-form-checkbox>
              </div>
            </b-nav-item>
            <!-- Started count -->
            <b-nav-item
              v-if="(checkLocation('desktops') || checkLocation('deployment_videowall')) && !creationMode"
              disabled
              class="d-none d-md-inline ml-4"
            >
              <b-icon
                icon="display-fill"
                aria-hidden="true"
                class="text-medium-gray mr-2 mr-lg-0"
              />
            </b-nav-item>
            <b-nav-item
              v-if="(checkLocation('desktops') || checkLocation('deployment_videowall')) && !creationMode"
              disabled
            >
              <span class="d-none d-lg-inline text-medium-gray">{{ `${$t("components.statusbar.desktops-started")}:` }}</span><span class="text-medium-gray">{{ ` ${startedDesktops}` }}</span>
            </b-nav-item>
          </b-navbar-nav>

          <!-- Right aligned nav items-->
          <div class="pt-1">
            <b-button
              v-if="checkLocation('desktops') && !creationMode"
              :pill="true"
              class="mr-0 mr-md-4"
              variant="outline-primary"
              size="sm"
              @click="createDesktop()"
            >
              {{ `${$t("components.statusbar.new-desktop")}` }}
            </b-button>
          </div>
          <div class="pt-1">
            <b-button
              v-if="checkLocation('deployments') && !creationMode"
              :pill="true"
              class="mr-0 mr-md-4"
              variant="outline-primary"
              size="sm"
              @click="navigate('deploymentsnew')"
            >
              {{ `${$t("components.statusbar.new-deployment")}` }}
            </b-button>
          </div>
          <div class="pt-1">
            <b-button
              v-if="checkLocation('media') && !creationMode"
              :pill="true"
              class="mr-0 mr-md-4"
              variant="outline-primary"
              size="sm"
              @click="createMedia()"
            >
              {{ `${$t("components.statusbar.new-media")}` }}
            </b-button>
          </div>
          <div
            v-if="checkLocation('deployment_desktops')"
            class="pt-1"
          >
            <!-- <b-button
              class="rounded-circle px-2 mr-2 btn-green"
              :title="$t('components.statusbar.deployment.buttons.start.title')"
              @click="startDesktops()"
            >
              <b-icon
                icon="play"
                scale="0.75"
              />
            </b-button> -->
            <b-button
              class="rounded-circle px-2 mr-2 btn-red"
              :title="$t('components.statusbar.deployment.buttons.stop.title')"
              @click="stopDesktops()"
            >
              <b-icon
                icon="stop"
                scale="0.75"
              />
            </b-button>
            <b-button
              class="rounded-circle px-2 mr-2"
              :class="visibleClass()"
              :title="deployment.visible ? $t('components.statusbar.deployment.buttons.make-not-visible.title') : $t('components.statusbar.deployment.buttons.make-visible.title')"
              @click="toggleVisible()"
            >
              <b-icon
                :icon="toggleVisibleIcon()"
                scale="0.75"
              />
            </b-button>
            <b-button
              class="rounded-circle px-2 mr-2 btn-dark-blue"
              :title="$t('components.statusbar.deployment.buttons.videowall.title')"
              @click="goToVideowall()"
            >
              <b-icon
                icon="grid-fill"
                scale="0.75"
              />
            </b-button>
            <b-button
              class="rounded-circle btn-purple px-2 mr-2"
              :title="$t('components.statusbar.deployment.buttons.download-direct-viewer.title')"
              @click="downloadDirectViewerCSV()"
            >
              <b-icon
                icon="download"
                scale="0.75"
              />
            </b-button>
            <b-button
              class="rounded-circle px-2 mr-2 btn-orange"
              :title="$t('components.statusbar.deployment.buttons.recreate.title')"
              @click="recreateDeployment()"
            >
              <b-icon
                icon="arrow-clockwise"
                scale="0.75"
              />
            </b-button>
            <b-button
              class="rounded-circle btn-red px-2 mr-2"
              :title="$t('components.statusbar.deployment.buttons.delete.title')"
              @click="deleteDeployment()"
            >
              <b-icon
                icon="trash-fill"
                scale="0.75"
              />
            </b-button>
          </div>
          <b-navbar-nav
            v-if="checkLocation('desktops') && !creationMode"
            class="ml-auto flex-row d-none d-xl-flex"
          >
            <b-nav-item
              href="#"
              :class="{selectedView: viewType === 'grid'}"
              @click="changeView('grid')"
            >
              <b-icon
                icon="grid-fill"
                aria-hidden="true"
                class="text-medium-gray mt-1"
              />
            </b-nav-item>
            <b-nav-item
              href="#"
              :class="{selectedView: viewType === 'list'}"
              class="ml-sm-2 ml-xl-0"
              @click="changeView('list')"
            >
              <b-icon
                icon="list"
                aria-hidden="true"
                class="text-medium-gray mt-1"
              />
            </b-nav-item>
          </b-navbar-nav>
          <!-- Videowall grid and individual view -->
          <b-navbar-nav
            v-if="checkLocation('deployment_videowall')"
            class="ml-auto flex-row d-none d-xl-flex"
          >
            <b-nav-item
              href="#"
              :class="{selectedView: viewType === 'grid'}"
              @click="changeView('grid')"
            >
              <b-icon
                icon="grid-fill"
                aria-hidden="true"
                class="text-medium-gray mt-1"
              />
            </b-nav-item>
            <b-nav-item
              href="#"
              :class="{selectedView: viewType === 'youtube'}"
              class="ml-sm-2 ml-xl-0"
              @click="changeView('youtube')"
            >
              <b-icon
                icon="grid1x2-fill"
                aria-hidden="true"
                class="text-medium-gray mt-1"
              />
            </b-nav-item>
          </b-navbar-nav>
        </div>
      </b-navbar>
    </b-container>
  </div>
</template>

<script>
import { desktopStates } from '@/shared/constants'
import DesktopsFilter from '@/components/desktops/DesktopsFilter.vue'
import VisibilityModal from '@/components/deployments/VisibilityModal.vue'
import { ref, computed, watch } from '@vue/composition-api'
import i18n from '@/i18n'

export default {
  components: {
    DesktopsFilter,
    VisibilityModal
  },
  setup (props, context) {
    const $store = context.root.$store

    const started = ref(false)

    const createDesktop = () => {
      $store.dispatch('checkCreateQuota', { itemType: 'desktops', routeName: 'desktopsnew' })
    }

    const createMedia = () => {
      $store.dispatch('checkCreateQuota', { itemType: 'media', routeName: 'medianew' })
    }

    const deployment = computed(() => $store.getters.getDeployment)
    const desktops = computed(() => $store.getters.getDesktops)
    const viewType = computed(() => $store.getters.getViewType)

    const goToDeployments = () => {
      context.root.$router.push({ name: 'deployments' })
    }

    const urlTokens = computed(() => $store.getters.getUrlTokens)

    const creationMode = computed(() => urlTokens.value.includes('new'))

    const checkLocation = (location) => {
      const tokens = urlTokens.value
      return tokens === location
    }

    const startedDesktops = computed(() => {
      const allDesktops = checkLocation('desktops') ? desktops.value : deployment.value.desktops
      const startedDesktops = allDesktops.filter((item) => {
        return item && [desktopStates.started, desktopStates.waitingip, desktopStates['shutting-down']].includes(item.state.toLowerCase())
      })
      return startedDesktops.length
    })

    // Deployment buttons
    const startDesktops = () => {
      context.root.$snotify.clear()

      const yesAction = () => {
        context.root.$snotify.clear()
        $store.dispatch('startDeploymentDesktops', { id: deployment.value.id })
      }

      const noAction = (toast) => {
        context.root.$snotify.clear()
      }

      context.root.$snotify.prompt(`${i18n.t('messages.confirmation.start-deployment-desktops', { name: deployment.value.name })}`, {
        position: 'centerTop',
        buttons: [
          { text: `${i18n.t('messages.yes')}`, action: yesAction, bold: true },
          { text: `${i18n.t('messages.no')}`, action: noAction }
        ],
        placeholder: ''
      })
    }

    const stopDesktops = () => {
      context.root.$snotify.clear()

      const yesAction = () => {
        context.root.$snotify.clear()
        $store.dispatch('stopDeploymentDesktops', { id: deployment.value.id })
      }

      const noAction = (toast) => {
        context.root.$snotify.clear()
      }

      context.root.$snotify.prompt(`${i18n.t('messages.confirmation.stop-deployment-desktops', { name: deployment.value.name })}`, {
        position: 'centerTop',
        buttons: [
          { text: `${i18n.t('messages.yes')}`, action: yesAction, bold: true },
          { text: `${i18n.t('messages.no')}`, action: noAction }
        ],
        placeholder: ''
      })
    }

    const redirectDeployment = () => {
      context.root.$router.push({ name: 'deployment_desktops', params: { id: deployment.value.id } })
    }

    const visibleClass = () => {
      return deployment.value.visible ? 'btn-blue' : 'btn-grey'
    }

    const toggleVisibleIcon = () => {
      return deployment.value.visible ? 'eye-fill' : 'eye-slash-fill'
    }

    const goToVideowall = () => {
      context.root.$router.push({ name: 'deployment_videowall', params: { id: deployment.value.id } })
    }

    const toggleVisible = () => {
      $store.dispatch('updateVisibilityModal', {
        show: true,
        item: { id: deployment.value.id, visible: deployment.value.visible, stopStartedDomains: false }
      })
    }

    const downloadDirectViewerCSV = () => {
      context.root.$snotify.clear()

      const resetJumperUrls = () => {
        context.root.$snotify.clear()
        $store.dispatch('downloadDirectViewerCSV', { id: deployment.value.id, reset: true })
      }

      const downloadCsv = () => {
        context.root.$snotify.clear()
        $store.dispatch('downloadDirectViewerCSV', { id: deployment.value.id })
      }

      context.root.$snotify.confirm(`${i18n.t('messages.confirmation.direct-viewer-reset')}`, {
        position: 'centerTop',
        buttons: [
          { text: `${i18n.t('messages.yes')}`, action: resetJumperUrls, bold: true },
          { text: `${i18n.t('messages.no')}`, action: downloadCsv }
        ],
        placeholder: ''
      })
    }

    const deleteDeployment = () => {
      context.root.$snotify.clear()

      const yesAction = () => {
        context.root.$snotify.clear()
        $store.dispatch('deleteDeployment', { id: deployment.value.id, path: 'deployments' })
      }

      const noAction = (toast) => {
        context.root.$snotify.clear()
      }

      context.root.$snotify.prompt(`${i18n.t('messages.confirmation.delete-deployment', { name: deployment.value.name })}`, {
        position: 'centerTop',
        buttons: [
          { text: `${i18n.t('messages.yes')}`, action: yesAction, bold: true },
          { text: `${i18n.t('messages.no')}`, action: noAction }
        ],
        placeholder: ''
      })
    }

    const recreateDeployment = () => {
      context.root.$snotify.clear()

      const yesAction = () => {
        context.root.$snotify.clear()
        $store.dispatch('recreateDeployment', { id: deployment.value.id })
      }

      const noAction = (toast) => {
        context.root.$snotify.clear()
      }

      context.root.$snotify.prompt(`${i18n.t('messages.confirmation.recreate-deployment', { name: deployment.value.name })}`, {
        position: 'centerTop',
        buttons: [
          { text: `${i18n.t('messages.yes')}`, action: yesAction, bold: true },
          { text: `${i18n.t('messages.no')}`, action: noAction }
        ],
        placeholder: ''
      })
    }

    const startedFilter = () => {
      started.value = !started.value
      if (checkLocation('desktops')) {
        $store.dispatch('toggleShowStarted')
      } else if (checkLocation('deployment_videowall')) {
        $store.dispatch('toggleDeploymentsShowStarted')
      }
    }
    const changeView = (type) => {
      $store.dispatch('setViewType', type)
    }

    watch(() => context.root.$route, () => {
      started.value = false
      $store.dispatch('setViewType', 'grid')
    }, { immediate: true })

    const navigate = (path) => {
      $store.dispatch('navigate', path)
    }

    return {
      goToDeployments,
      startDesktops,
      stopDesktops,
      deployment,
      visibleClass,
      toggleVisibleIcon,
      redirectDeployment,
      goToVideowall,
      toggleVisible,
      downloadDirectViewerCSV,
      deleteDeployment,
      recreateDeployment,
      createDesktop,
      createMedia,
      started,
      checkLocation,
      changeView,
      startedFilter,
      startedDesktops,
      creationMode,
      navigate,
      viewType
    }
  },
  mutations: {
    setVisibilityModal: (state, visibilityModal) => {
      state.visibilityModal = visibilityModal
    }
  }
}
</script>
