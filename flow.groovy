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
  sh "tar -c -f buildout.tar bin parts src"
  archive 'buildout.tar'
}

stage 'Test'
parallel(
  alltests: {
    node {
      prepareBuildout()
      sh "bin/jenkins-alltests --group=Plone"
      sh "find parts"
      // step([$class: 'JUnitResultArchiver', testResults: 'parts/jenkins-test/testreports/*.xml'])
    }
  },
  alltestsat: {
    node {
      prepareBuildout()
      sh "bin/jenkins-alltests-at --group=AT_plone_app_testing"
      sh "find parts"
      // step([$class: 'JUnitResultArchiver', testResults: 'parts/jenkins-test/testreports/*.xml'])
    }
  }
)

stage 'Notification'
node {
  step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: 'tisto@plone.org', sendToIndividuals: true])
}


/**
* Prepare buildout by cleaning up the workspace, and fetching buildout.
*/
def prepareBuildout() {
  sh "rm -rf *"
  unarchive mapping: ['buildout.tar': '.']
  sh "tar -x -f buildout.tar"
}
