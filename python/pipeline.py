class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):

        if project.has_tests():
            if "success" == project.run_tests():
                self.log.info("Tests passed")
                tests_passed = True
            else:
                self.log.error("Tests failed")
                tests_passed = False
        else:
            self.log.info("No tests")
            tests_passed = True

        if tests_passed:
            if "success" == project.deploy():
                self.log.info("Deployment successful")
                deploy_successful = True
            else:
                self.log.error("Deployment failed")
                deploy_successful = False
        else:
            deploy_successful = False

        summary = self.create_summary(deploy_successful, tests_passed)
        self.send_email_summary(summary)

    def send_email_summary(self, summary):
        if self.config.send_email_summary():
            self.log.info("Sending email")
            self.emailer.send(summary)
        else:
            self.log.info("Email disabled")

    def create_summary(self, deploy_successful, tests_passed):
        if tests_passed:
            if deploy_successful:
                return "Deployment completed successfully"
            else:
                return "Deployment failed"
        else:
            return "Tests failed"
