import groovy.json.JsonOutput

/** Tox environment */
def environment = 'tests'

/** Map of desired capabilities */
def capabilities = [
  browserName: 'Firefox',
  version: '47.0',
  platform: 'Windows 7'
]

/** Write capabilities to JSON file
 *
 * @param desiredCapabilities capabilities to include in the file
*/
def writeCapabilities(desiredCapabilities) {
    def defaultCapabilities = [
        build: env.BUILD_TAG,
        public: 'public restricted'
    ]
    def capabilities = defaultCapabilities.clone()
    capabilities.putAll(desiredCapabilities)
    def json = JsonOutput.toJson([capabilities: capabilities])
    writeFile file: 'capabilities.json', text: json
}

/** Run Tox
 *
 * @param environment test environment to run
*/
def runTox(environment) {
  def processes = env.PYTEST_PROCESSES ?: 'auto'
  try {
    wrap([$class: 'AnsiColorBuildWrapper']) {
      withCredentials([[
        $class: 'StringBinding',
        credentialsId: 'SAUCELABS_API_KEY',
        variable: 'SAUCELABS_API_KEY']]) {
        withEnv(["PYTEST_ADDOPTS=${PYTEST_ADDOPTS} " +
          "-n=${processes} " +
          "--driver=SauceLabs " +
          "--variables=capabilities.json " +
          "--color=yes"]) {
          sh "tox -e ${environment}"
        }
      }
    }
  } catch(err) {
    currentBuild.result = 'FAILURE'
    throw err
  } finally {
    dir('results') {
      stash environment
    }
  }
}

/** Send a notice to #fxtest-alerts on irc.mozilla.org with the build result
 *
 * @param result outcome of build
*/
def ircNotification(result) {
  def nick = "fxtest${BUILD_NUMBER}"
  def channel = '#fx-test-alerts'
  result = result.toUpperCase()
  def message = "Project ${JOB_NAME} build #${BUILD_NUMBER}: ${result}: ${BUILD_URL}"
  node {
    sh """
        (
        echo NICK ${nick}
        echo USER ${nick} 8 * : ${nick}
        sleep 5
        echo "JOIN ${channel}"
        echo "NOTICE ${channel} :${message}"
        echo QUIT
        ) | openssl s_client -connect irc.mozilla.org:6697
    """
  }
}

stage('Checkout') {
  node {
    timestamps {
      deleteDir()
      checkout scm
      stash 'workspace'
    }
  }
}

stage('Lint') {
  node {
    timestamps {
      deleteDir()
      unstash 'workspace'
      sh 'tox -e flake8'
    }
  }
}

try {
  stage('Test') {
    node {
      timeout(time: 1, unit: 'HOURS') {
        timestamps {
          deleteDir()
          unstash 'workspace'
          try {
            writeCapabilities(capabilities)
            runTox(environment)
          } catch(err) {
            currentBuild.result = 'FAILURE'
            throw err
          } finally {
            dir('results') {
              stash environment
            }
          }
        }
      }
    }
  }
} catch(err) {
  currentBuild.result = 'FAILURE'
  ircNotification(currentBuild.result)
  mail(
    body: "${BUILD_URL}",
    from: "firefox-test-engineering@mozilla.com",
    replyTo: "firefox-test-engineering@mozilla.com",
    subject: "Build failed in Jenkins: ${JOB_NAME} #${BUILD_NUMBER}",
    to: "fte-ci@mozilla.com")
  throw err
} finally {
  stage('Results') {
    node {
      deleteDir()
      sh 'mkdir results'
      dir('results') {
        unstash environment
      }
      publishHTML(target: [
        allowMissing: false,
        alwaysLinkToLastBuild: true,
        keepAll: true,
        reportDir: 'results',
        reportFiles: "${environment}.html",
        reportName: 'HTML Report'])
      junit 'results/*.xml'
      archiveArtifacts 'results/*'
    }
  }
}
