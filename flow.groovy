stage 'Build'
node {
  sh "rm -rf ./*"
  git branch: '5.0', changelog: true, poll: true, url: 'https://github.com/plone/buildout.coredev.git'
  sh "python2.7 bootstrap.py"
  sh "bin/buildout -c jenkins.cfg"
  step([$class: 'ArtifactArchiver', artifacts: '**/.*', fingerprint: true])
}

stage name: 'Test'
parallel(
  test1: {
    node {
      unarchive mapping: ['**/*': '.']
      sh "bin/buildout -c jenkins.cfg"
      sh "bin/jenkins-test -s plone.app.discussion"
      step([$class: 'ArtifactArchiver', artifacts: 'parts/jenkins-test/testreports/*.xml', fingerprint: true])
      step([$class: 'JUnitResultArchiver', testResults: 'parts/jenkins-test/testreports/*.xml'])
    }
  },
  test2: {
    node {
      unarchive mapping: ['**/*': '.']
      sh "ls -al"
      sh "bin/buildout -c jenkins.cfg"
      sh "bin/jenkins-test -s plone.app.dexterity"
      step([$class: 'ArtifactArchiver', artifacts: 'parts/jenkins-test/testreports/*.xml', fingerprint: true])
      step([$class: 'JUnitResultArchiver', testResults: 'parts/jenkins-test/testreports/*.xml'])
    }
  }
)
