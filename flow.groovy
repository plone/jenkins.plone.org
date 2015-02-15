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
  alltest: {
    node {
      sh "rm -rf *"
      unarchive mapping: ['buildout.tar': '.']
      sh "tar -x -f buildout.tar"
      sh "bin/jenkins-alltests"
      step([$class: 'JUnitResultArchiver', testResults: 'parts/jenkins-test/testreports/*.xml'])
    }
  },
  alltestat: {
    node {
      sh "rm -rf *"
      unarchive mapping: ['buildout.tar': '.']
      sh "tar -x -f buildout.tar"
      sh "bin/jenkins-alltests-at"
      step([$class: 'JUnitResultArchiver', testResults: 'parts/jenkins-test/testreports/*.xml'])
    }
  }
)

stage 'Notification'
node {
  stage 'Notification'
  step([$class: 'Mailer', notifyEveryUnstableBuild: true, recipients: 'tisto@plone.org', sendToIndividuals: true])
}
