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
  alltests: {
    node {
      prepareBuildout()
      try {
        sh "bin/alltests --xml"
        step([$class: 'JUnitResultArchiver', testResults: 'parts/test/testreports/*.xml'])
      } catch (e) {
        def w = new StringWriter()
        e.printStackTrace(new PrintWriter(w))
        mail subject: "alltests failed with ${e.message}", to: 'tisto@plone.org', body: "Failed: ${w}"
        throw e
      }
    }
  },
  alltestsat: {
    node {
      prepareBuildout()
      try {
        sh "bin/alltests-at --xml"
        step([$class: 'JUnitResultArchiver', testResults: 'parts/test/testreports/*.xml'])
      } catch (e) {
        def w = new StringWriter()
        e.printStackTrace(new PrintWriter(w))
        mail subject: "alltests-at failed with ${e.message}", to: 'tisto@plone.org', body: "Failed: ${w}"
        throw e
      }
    }
  },
  robot: {
    node {
      prepareBuildout()
      wrap([$class: 'Xvfb']) {
        sh "bin/alltests -t ONLYROBOT --all --xml"
      }
    }
  }
)

stage 'Notification'
node {
  step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: 'tisto@plone.org', sendToIndividuals: true])
  mail (to: 'tisto@plone.org',
         subject: "Job '${env.JOB_NAME}' (${env.BUILD_NUMBER}) is ready.",
         body: "Please go to ${env.BUILD_URL}.");
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
