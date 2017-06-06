pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        parallel(
          "Build": {
            sh 'echo \'build\''
            
          },
          "Build Check": {
            echo 'Build Check done'
            
          }
        )
      }
    }
    stage('Test') {
      steps {
        parallel(
          "Test": {
            sh 'echo \'Test\''
            
          },
          "": {
            echo 'Test done'
            
          }
        )
      }
    }
    stage('Deploy') {
      steps {
        parallel(
          "Deploy": {
            sh 'echo \'Deploy\''
            
          },
          "": {
            echo 'Deploy done'
            
          }
        )
      }
    }
  }
}