class TestsFailedException(Exception):
    pass


class DeploymentFailedException(Exception):
    pass


class Pipeline:
    def __init__(self, config, emailer, log):
        self.config = config
        self.emailer = emailer
        self.log = log

    def run(self, project):

        try:
            self.run_test_if_test(project)
            self.deploy_project(project)
            self.send_email_summary("Deployment completed successfully")
        except TestsFailedException:
            self.send_email_summary("Tests failed")
        except DeploymentFailedException:
            self.send_email_summary("Deployment failed")

    def deploy_project(self, project):
        if "success" != project.deploy():
            self.log.error("Deployment failed")
            raise DeploymentFailedException

        self.log.info("Deployment successful")

    def run_test_if_test(self, project):
        if not project.has_tests():
            self.log.info("No tests")
            return

        self.run_test(project)

    def run_test(self, project):
        if "success" != project.run_tests():
            self.log.error("Tests failed")
            raise TestsFailedException

        self.log.info("Tests passed")

    def send_email_summary(self, summary):
        if not self.config.send_email_summary():
            self.log.info("Email disabled")
            return

        self.log.info("Sending email")
        self.emailer.send(summary)
