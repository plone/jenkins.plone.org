/**
 * Run and archive buildout, then pass it to the next stage.
 */
stage 'Build'
node {
  sh "rm -rf *"
  git branch: '5.0', changelog: true, poll: true, url: 'https://github.com/plone/buildout.coredev.git'
  sh "python2.7 bootstrap.py"
  sh "bin/buildout -c jenkins.cfg"
  sh "tar -c -f buildout.tar bin parts develop-eggs var src"
  archive 'buildout.tar'
}

stage 'Test'
node {
  sh "rm -rf *"
  unarchive mapping: ['buildout.tar': '.']
  sh "tar -x -f buildout.tar"
  sh "ls -al"
  sh "bin/test -s plone.app.discussion"
}
