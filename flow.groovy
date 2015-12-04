/**
 * Run buildout coredev, archive it and pass it to the test stage that runs
 * test in parallel.
 */

stage 'Build'
node {
  sh "rm -rf *"
  git branch: '5.0', changelog: true, poll: true, url: 'https://github.com/plone/buildout.coredev.git'
  sh "python2.7 bootstrap.py -c jenkins.cfg"
  sh "bin/buildout -c jenkins.cfg"
  sh "tar -c -f buildout.tar bin parts src *.cfg"
  archive 'buildout.tar'
}

stage 'Test'
parallel(
  tests: {
    node {
      prepareBuildout()
      try {
        sh "bin/alltests --xml"
        step([$class: 'JUnitResultArchiver', testResults: 'parts/test/testreports/*.xml'])
      } catch (e) {
        mail subject: "Jenkins Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) failed in the alltests stage with ${e.message}", to: 'tisto@plone.org', body: "Please go to ${env.BUILD_URL}."
        throw e
      }
    }
  },
  archetypes: {
    node {
      prepareBuildout()
      try {
        sh "bin/alltests-at --xml"
        step([$class: 'JUnitResultArchiver', testResults: 'parts/test/testreports/*.xml'])
      } catch (e) {mail subject: "Jenkins Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) failed in the alltests-at stage with ${e.message}", to: 'tisto@plone.org', body: "Please go to ${env.BUILD_URL}."
        throw e
      }
    }
  },
  robot: {
    node {
      prepareBuildout()
      wrap([$class: 'Xvfb']) {
        try {
          sh "bin/alltests -t ONLYROBOT --all --xml"
          //step([$class: 'JUnitResultArchiver', testResults: 'parts/test/testreports/*.xml'])
          /*
          step([$class: 'RobotPublisher',
            disableArchiveOutput: false,
            logFileName: 'log.html',
            onlyCritical: true,
            otherFiles: '',
            outputFileName: 'output.xml',
            outputPath: '.',
            passThreshold: 90,
            reportFileName: 'report.html',
            unstableThreshold: 100]);
          */
        } catch (e) {
          mail subject: "Jenkins Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) failed in the alltests-robot stage with ${e.message}", to: 'tisto@plone.org', body: "Please go to ${env.BUILD_URL}."
          throw e
        }

      }
    }
  }
)

stage 'Notification'
node {
  step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: 'tisto@plone.org', sendToIndividuals: true])
  mail (
    to: 'tisto@plone.org',
    subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) is ready.",
    body: "Please go to ${env.BUILD_URL}."
  );
}


/**
* Prepare buildout by cleaning up the workspace, and fetching buildout.
*/
def prepareBuildout() {
  sh "rm -rf *"
  unarchive mapping: ['buildout.tar': '.']
  sh "tar -x -f buildout.tar"
  sh "bin/buildout -c jenkins.cfg"
}
