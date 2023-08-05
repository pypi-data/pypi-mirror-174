'''
# CDK Pipelines for GitHub Workflows

![cdk-constructs: Experimental](https://img.shields.io/badge/cdk--constructs-experimental-important.svg?style=for-the-badge)

[![View on Construct Hub](https://constructs.dev/badge?package=cdk-pipelines-github)](https://constructs.dev/packages/cdk-pipelines-github)

> The APIs in this module are experimental and under active development.
> They are subject to non-backward compatible changes or removal in any future version. These are
> not subject to the [Semantic Versioning](https://semver.org/) model and breaking changes will be
> announced in the release notes. This means that while you may use them, you may need to update
> your source code when upgrading to a newer version of this package.

A construct library for painless Continuous Delivery of CDK applications,
deployed via
[GitHub Workflows](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions).

The CDK already has a CI/CD solution,
[CDK Pipelines](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines-readme.html),
which creates an AWS CodePipeline that deploys CDK applications. This module
serves the same surface area, except that it is implemented with GitHub
Workflows.

## Table of Contents

* [CDK Pipelines for GitHub Workflows](#cdk-pipelines-for-github-workflows)

  * [Table of Contents](#table-of-contents)
  * [Usage](#usage)
  * [Initial Setup](#initial-setup)
  * [AWS Credentials](#aws-credentials)

    * [GitHub Action Role](#github-action-role)

      * [`GitHubActionRole` Construct](#githubactionrole-construct)
    * [GitHub Secrets](#github-secrets)
    * [Runners with Preconfigured Credentials](#runners-with-preconfigured-credentials)
    * [Using Docker in the Pipeline](#using-docker-in-the-pipeline)

      * [Authenticating to Docker registries](#authenticating-to-docker-registries)
  * [Runner Types](#runner-types)

    * [GitHub Hosted Runner](#github-hosted-runner)
    * [Self Hosted Runner](#self-hosted-runner)
  * [Escape Hatches](#escape-hatches)
  * [Additional Features](#additional-features)

    * [GitHub Action Step](#github-action-step)
    * [Configure GitHub Environment](#configure-github-environment)

      * [Manual Approval Step](#manual-approval-step)
    * [Pipeline YAML Comments](#pipeline-yaml-comments)
  * [Tutorial](#tutorial)
  * [Not supported yet](#not-supported-yet)
  * [Contributing](#contributing)
  * [License](#license)

## Usage

Assuming you have a
[`Stage`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Stage.html)
called `MyStage` that includes CDK stacks for your app and you want to deploy it
to two AWS environments (`BETA_ENV` and `PROD_ENV`):

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  awsCreds: AwsCredentials.fromOpenIdConnect({
    gitHubActionRoleArn: 'arn:aws:iam::<account-id>:role/GitHubActionRole',
  }),
});

pipeline.addStage(new MyStage(app, 'Beta', { env: BETA_ENV }));
pipeline.addStage(new MyStage(app, 'Prod', { env: PROD_ENV }));

app.synth();
```

When you run `cdk synth`, a `deploy.yml` workflow will be created under
`.github/workflows` in your repo. This workflow will deploy your application
based on the definition of the pipeline. In the example above, it will deploy
the two stages in sequence, and within each stage, it will deploy all the
stacks according to their dependency order and maximum parallelism. If your app
uses assets, assets will be published to the relevant destination environment.

The `Pipeline` class from `cdk-pipelines-github` is derived from the base CDK
Pipelines class, so most features should be supported out of the box. See the
[CDK Pipelines](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines-readme.html)
documentation for more details.

**NOTES:**

* Environments must be bootstrapped separately using `cdk bootstrap`. See [CDK
  Environment
  Bootstrapping](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.pipelines-readme.html#cdk-environment-bootstrapping)
  for details.

## Initial Setup

Assuming you have your CDK app checked out on your local machine, here are the suggested steps
to develop your GitHub Workflow.

* Set up AWS Credentials your local environment. It is highly recommended to authenticate via an OpenId
  Connect IAM Role. You can set one up using the [`GithubActionRole`](#github-action-role) class provided
  in this module. For more information (and alternatives), see [AWS Credentials](#aws-credentials).
* When you've updated your pipeline and are ready to deploy, run `cdk synth`. This creates a workflow file
  in `.github/workflows/deploy.yml`.
* When you are ready to test your pipeline, commit your code changes as well as the `deploy.yml` file to
  GitHub. GitHub will automatically try to run the workflow found under `.github/workflows/deploy.yml`.
* You will be able to see the result of the run on the `Actions` tab in your repository:

  ![Screen Shot 2021-08-22 at 12 06 05](https://user-images.githubusercontent.com/598796/130349345-a10a2f75-0848-4de8-bc4c-f5a1418ee228.png)

For an in-depth run-through on creating your own GitHub Workflow, see the
[Tutorial](#tutorial) section.

## AWS Credentials

There are two ways to supply AWS credentials to the workflow:

* GitHub Action IAM Role (recommended).
* Long-lived AWS Credentials stored in GitHub Secrets.

The GitHub Action IAM Role authenticates via the GitHub OpenID Connect provider
and is recommended, but it requires preparing your AWS account beforehand. This
approach allows your Workflow to exchange short-lived tokens directly from AWS.
With OIDC, benefits include:

* No cloud secrets.
* Authentication and authorization management.
* Rotating credentials.

You can read more
[here](https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/about-security-hardening-with-openid-connect).

### GitHub Action Role

Authenticating via OpenId Connect means you do not need to store long-lived
credentials as GitHub Secrets. With OIDC, you provide a pre-provisioned IAM
role to your GitHub Workflow via the `awsCreds.fromOpenIdConnect` API:

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  awsCreds: AwsCredentials.fromOpenIdConnect({
    gitHubActionRoleArn: 'arn:aws:iam::<account-id>:role/GitHubActionRole',
  }),
});
```

There are two ways to create this IAM role:

* Use the `GitHubActionRole` construct (recommended and described below).
* Manually set up the role ([Guide](https://github.com/cdklabs/cdk-pipelines-github/blob/main/GITHUB_ACTION_ROLE_SETUP.md)).

#### `GitHubActionRole` Construct

Because this construct involves creating an IAM role in your account, it must
be created separate to your GitHub Workflow and deployed via a normal
`cdk deploy` with your local AWS credentials. Upon successful deployment, the
arn of your newly created IAM role will be exposed as a `CfnOutput`.

To utilize this construct, create a separate CDK stack with the following code
and `cdk deploy`:

```python
import { GitHubActionRole } from 'cdk-pipelines-github';
import { App, Construct, Stack, StackProps } from 'aws-cdk-lib';

class MyGitHubActionRole extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const provider = new GitHubActionRole(this, 'github-action-role', {
      repoString: 'myUser/myRepo',
    };
  }
}

const app = new App();
new MyGitHubActionRole(app, 'MyGitHubActionRole');
app.synth();
```

Note: If you have previously created the GitHub identity provider with url
`https://token.actions.githubusercontent.com`, the above example will fail
because you can only have one such provider defined per account. In this
case, you must provide the already created provider into your `GithubActionRole`
construct via the `provider` property.

> Make sure the audience for the provider is `sts.amazonaws.com` in this case.

```python
class MyGitHubActionRole extends Stack {
  constructor(scope: Construct, id: string, props?: StackProps) {
    super(scope, id, props);

    const provider = new GitHubActionRole(this, 'github-action-role', {
      repos: ['myUser/myRepo'],
      provider: GitHubActionRole.existingGitHubActionsProvider(this),
    });
  }
}
```

### GitHub Secrets

Authenticating via this approach means that you will be manually creating AWS
credentials and duplicating them in GitHub secrets. The workflow expects the
GitHub repository to include secrets with AWS credentials under
`AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY`. You can override these defaults
by supplying the `awsCreds.fromGitHubSecrets` API to the workflow:

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  awsCreds: AwsCredentials.fromGitHubSecrets({
    accessKeyId: 'MY_ID', // GitHub will look for the access key id under the secret `MY_ID`
    secretAccessKey: 'MY_KEY', // GitHub will look for the secret access key under the secret `MY_KEY`
  }),
});
```

### Runners with Preconfigured Credentials

If your runners provide credentials themselves, you can configure `awsCreds` to
skip passing credentials:

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  awsCreds: AwsCredentials.runnerHasPreconfiguredCreds(), // NO credentials will be provided.
});
```

### Using Docker in the Pipeline

You can use Docker in GitHub Workflows in a similar fashion to CDK Pipelines.
For a full discussion on how to use Docker in CDK Pipelines, see
[Using Docker in the Pipeline](https://github.com/aws/aws-cdk/blob/master/packages/@aws-cdk/pipelines/README.md#using-docker-in-the-pipeline).

Just like CDK Pipelines, you may need to authenticate to Docker registries to
avoid being throttled.

#### Authenticating to Docker registries

You can specify credentials to use for authenticating to Docker registries as
part of the Workflow definition. This can be useful if any Docker image assets —
in the pipeline or any of the application stages — require authentication, either
due to being in a different environment (e.g., ECR repo) or to avoid throttling
(e.g., DockerHub).

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  dockerCredentials: [
    // Authenticate to ECR
    DockerCredential.ecr('<account-id>.dkr.ecr.<aws-region>.amazonaws.com'),

    // Authenticate to DockerHub
    DockerCredential.dockerHub({
      // These properties are defaults; feel free to omit
      usernameKey: 'DOCKERHUB_USERNAME',
      personalAccessTokenKey: 'DOCKERHUB_TOKEN',
    }),

    // Authenticate to Custom Registries
    DockerCredential.customRegistry('custom-registry', {
      usernameKey: 'CUSTOM_USERNAME',
      passwordKey: 'CUSTOM_PASSWORD',
    }),
  ],
});
```

## Runner Types

You can choose to run the workflow in either a GitHub hosted or [self-hosted](https://docs.github.com/en/actions/hosting-your-own-runners/about-self-hosted-runners) runner.

### GitHub Hosted Runner

The default is `Runner.UBUNTU_LATEST`. You can override this as shown below:

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  runner: Runner.WINDOWS_LATEST,
});
```

### Self Hosted Runner

The following example shows how to configure the workflow to run on a self-hosted runner. Note that you do not need to pass in `self-hosted` explicitly as a label.

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  runner: Runner.selfHosted(['label1', 'label2']),
});
```

## Escape Hatches

You can override the `deploy.yml` workflow file post-synthesis however you like.

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow, JsonPatch } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
});

const deployWorkflow = pipeline.workflowFile;
// add `on: workflow_call: {}` to deploy.yml
deployWorkflow.patch(JsonPatch.add('/on/workflow_call', {}));
// remove `on: workflow_dispatch` from deploy.yml
deployWorkflow.patch(JsonPatch.remove('/on/workflow_dispatch'));
```

## Additional Features

Below is a compilation of additional features available for GitHub Workflows.

### GitHub Action Step

If you want to call a GitHub Action in a step, you can utilize the `GitHubActionStep`.
`GitHubActionStep` extends `Step` and can be used anywhere a `Step` type is allowed.

The `jobSteps` array is placed into the pipeline job at the relevant `jobs.<job_id>.steps` as [documented here](https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idsteps).

In this example,

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow, JsonPatch } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
});

// "Beta" stage with a pre-check that uses code from the repo and an action
const stage = new MyStage(app, 'Beta', { env: BETA_ENV });
pipeline.addStage(stage, {
  pre: [new GitHubActionStep('PreBetaDeployAction', {
    jobSteps: [
      {
        name: 'Checkout',
        uses: 'actions/checkout@v2',
      },
      {
        name: 'pre beta-deploy action',
        uses: 'my-pre-deploy-action@1.0.0',
        with: {
          'app-id': 1234,
          'secrets': 'my-secrets',
        },
      },
      {
        name: 'pre beta-deploy check',
        run: 'npm run preDeployCheck',
      },
    ],
  })],
});

app.synth();
```

### Configure GitHub Environment

You can run your GitHub Workflow in select
[GitHub Environments](https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment).
Via the GitHub UI, you can configure environments with protection rules and secrets, and reference
those environments in your CDK app. A workflow that references an environment must follow any
protection rules for the environment before running or accessing the environment's secrets.

Assuming (just like in the main [example](#usage)) you have a
[`Stage`](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.Stage.html)
called `MyStage` that includes CDK stacks for your app and you want to deploy it
to two AWS environments (`BETA_ENV` and `PROD_ENV`) as well as GitHub Environments
`beta` and `prod`:

```python
import { App } from 'aws-cdk-lib';
import { ShellStep } from 'aws-cdk-lib/pipelines';
import { GitHubWorkflow } from 'cdk-pipelines-github';

const app = new App();

const pipeline = new GitHubWorkflow(app, 'Pipeline', {
  synth: new ShellStep('Build', {
    commands: [
      'yarn install',
      'yarn build',
    ],
  }),
  awsCreds: AwsCredentials.fromOpenIdConnect({
    gitHubActionRoleArn: 'arn:aws:iam::<account-id>:role/GitHubActionRole',
  }),
});

pipeline.addStageWithGitHubOptions(new MyStage(this, 'Beta', {
  env: BETA_ENV,
  gitHubEnvironment: 'beta',
}));
pipeline.addStageWithGitHubOptions(new MyStage(this, 'Prod', {
  env: PROD_ENV,
  gitHubEnvironment: 'prod',
}));

app.synth();
```

#### Manual Approval Step

One use case for using GitHub Environments with your CDK Pipeline is to create a
manual approval step for specific environments via Environment protection rules.
From the GitHub UI, you can specify up to 5 required reviewers that must approve
before the deployment can proceed:

<img width="1134" alt="require-reviewers" src="https://user-images.githubusercontent.com/7248260/163494925-627f5ca7-a34e-48fa-bec7-1e4924ab6c0c.png">

For more information and a tutorial for how to set this up, see this
[discussion](https://github.com/cdklabs/cdk-pipelines-github/issues/162).

### Pipeline YAML Comments

An "AUTOMATICALLY GENERATED FILE..." comment will by default be added to the top
of the pipeline YAML. This can be overriden as desired to add additional context
to the pipeline YAML.

```python
const pipeline = new GitHubWorkflow(/* ... */);

pipeline.workflowFile.commentAtTop = `AUTOGENERATED FILE, DO NOT EDIT DIRECTLY!

Deployed stacks from this pipeline:
${STACK_NAMES.map((s)=>`- ${s}\n`)}`;
```

This will generate the normal `deploy.yml` file, but with the additional comments:

```yaml
# AUTOGENERATED FILE, DO NOT EDIT DIRECTLY!

# Deployed stacks from this pipeline:
# - APIStack
# - AuroraStack

name: deploy
on:
  push:
    branches:
< the rest of the pipeline YAML contents>
```

## Tutorial

You can find an example usage in [test/example-app.ts](./test/example-app.ts)
which includes a simple CDK app and a pipeline.

You can find a repository that uses this example here: [eladb/test-app-cdkpipeline](https://github.com/eladb/test-app-cdkpipeline).

To run the example, clone this repository and install dependencies:

```shell
cd ~/projects # or some other playground space
git clone https://github.com/cdklabs/cdk-pipelines-github
cd cdk-pipelines-github
yarn
```

Now, create a new GitHub repository and clone it as well:

```shell
cd ~/projects
git clone https://github.com/myaccount/my-test-repository
```

You'll need to set up AWS credentials in your environment. Note that this tutorial uses
long-lived GitHub secrets as credentials for simplicity, but it is recommended to set up
a GitHub OIDC role instead.

```shell
export AWS_ACCESS_KEY_ID=xxxx
export AWS_SECRET_ACCESS_KEY=xxxxx
```

Bootstrap your environments:

```shell
export CDK_NEW_BOOTSTRAP=1
npx cdk bootstrap aws://ACCOUNTID/us-east-1
npx cdk bootstrap aws://ACCOUNTID/eu-west-2
```

Now, run the `manual-test.sh` script when your working directory is the new repository:

```shell
cd ~/projects/my-test-repository
~/projects/cdk-piplines/github/test/manual-test.sh
```

This will produce a `cdk.out` directory and a `.github/workflows/deploy.yml` file.

Commit and push these files to your repo and you should see the deployment
workflow in action. Make sure your GitHub repository has `AWS_ACCESS_KEY_ID` and
`AWS_SECRET_ACCESS_KEY` secrets that can access the same account that you
synthesized against.

> In this tutorial, you are supposed to commit `cdk.out` (i.e. the code is pre-synthed).
> Do not do this in your app; you should always synth during the synth step of the GitHub
> workflow. In the example app this is achieved through the `preSynthed: true` option.
> It is for example purposes only and is not something you should do in your app.
>
> ```python
> const pipeline = new GitHubWorkflow(new App(), 'Pipeline', {
>   synth: new ShellStep('Build', {
>     commands: ['echo "nothing to do (cdk.out is committed)"'],
>   }),
>   // only the example app should do this. your app should synth in the synth step.
>   preSynthed: true,
> });
> ```

## Not supported yet

Most features that exist in CDK Pipelines are supported. However, as the CDK Pipelines
feature are expands, the feature set for GitHub Workflows may lag behind. If you see a
feature that you feel should be supported by GitHub Workflows, please open a GitHub issue
to track it.

## Contributing

See [CONTRIBUTING](CONTRIBUTING.md) for more information.

## License

This project is licensed under the Apache-2.0 License.
'''
import abc
import builtins
import datetime
import enum
import typing

import jsii
import publication
import typing_extensions

from typeguard import check_type

from ._jsii import *

import aws_cdk
import aws_cdk.aws_iam
import aws_cdk.pipelines
import constructs


@jsii.data_type(
    jsii_type="cdk-pipelines-github.AddGitHubStageOptions",
    jsii_struct_bases=[aws_cdk.pipelines.AddStageOpts],
    name_mapping={
        "post": "post",
        "pre": "pre",
        "stack_steps": "stackSteps",
        "git_hub_environment": "gitHubEnvironment",
        "job_settings": "jobSettings",
        "stack_capabilities": "stackCapabilities",
    },
)
class AddGitHubStageOptions(aws_cdk.pipelines.AddStageOpts):
    def __init__(
        self,
        *,
        post: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
        pre: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[aws_cdk.pipelines.StackSteps, typing.Dict[str, typing.Any]]]] = None,
        git_hub_environment: typing.Optional[builtins.str] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
    ) -> None:
        '''Options to pass to ``addStageWithGitHubOpts``.

        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions
        :param git_hub_environment: Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']
        '''
        if isinstance(job_settings, dict):
            job_settings = JobSettings(**job_settings)
        if __debug__:
            def stub(
                *,
                post: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
                pre: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
                stack_steps: typing.Optional[typing.Sequence[typing.Union[aws_cdk.pipelines.StackSteps, typing.Dict[str, typing.Any]]]] = None,
                git_hub_environment: typing.Optional[builtins.str] = None,
                job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
                stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument post", value=post, expected_type=type_hints["post"])
            check_type(argname="argument pre", value=pre, expected_type=type_hints["pre"])
            check_type(argname="argument stack_steps", value=stack_steps, expected_type=type_hints["stack_steps"])
            check_type(argname="argument git_hub_environment", value=git_hub_environment, expected_type=type_hints["git_hub_environment"])
            check_type(argname="argument job_settings", value=job_settings, expected_type=type_hints["job_settings"])
            check_type(argname="argument stack_capabilities", value=stack_capabilities, expected_type=type_hints["stack_capabilities"])
        self._values: typing.Dict[str, typing.Any] = {}
        if post is not None:
            self._values["post"] = post
        if pre is not None:
            self._values["pre"] = pre
        if stack_steps is not None:
            self._values["stack_steps"] = stack_steps
        if git_hub_environment is not None:
            self._values["git_hub_environment"] = git_hub_environment
        if job_settings is not None:
            self._values["job_settings"] = job_settings
        if stack_capabilities is not None:
            self._values["stack_capabilities"] = stack_capabilities

    @builtins.property
    def post(self) -> typing.Optional[typing.List[aws_cdk.pipelines.Step]]:
        '''Additional steps to run after all of the stacks in the stage.

        :default: - No additional steps
        '''
        result = self._values.get("post")
        return typing.cast(typing.Optional[typing.List[aws_cdk.pipelines.Step]], result)

    @builtins.property
    def pre(self) -> typing.Optional[typing.List[aws_cdk.pipelines.Step]]:
        '''Additional steps to run before any of the stacks in the stage.

        :default: - No additional steps
        '''
        result = self._values.get("pre")
        return typing.cast(typing.Optional[typing.List[aws_cdk.pipelines.Step]], result)

    @builtins.property
    def stack_steps(self) -> typing.Optional[typing.List[aws_cdk.pipelines.StackSteps]]:
        '''Instructions for stack level steps.

        :default: - No additional instructions
        '''
        result = self._values.get("stack_steps")
        return typing.cast(typing.Optional[typing.List[aws_cdk.pipelines.StackSteps]], result)

    @builtins.property
    def git_hub_environment(self) -> typing.Optional[builtins.str]:
        '''Run the stage in a specific GitHub Environment.

        If specified,
        any protection rules configured for the environment must pass
        before the job is set to a runner. For example, if the environment
        has a manual approval rule configured, then the workflow will
        wait for the approval before sending the job to the runner.

        Running a workflow that references an environment that does not
        exist will create an environment with the referenced name.

        :default: - no GitHub environment

        :see: https://docs.github.com/en/actions/deployment/targeting-different-environments/using-environments-for-deployment
        '''
        result = self._values.get("git_hub_environment")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_settings(self) -> typing.Optional["JobSettings"]:
        '''Job level settings that will be applied to all jobs in the stage.

        Currently the only valid setting is 'if'.
        '''
        result = self._values.get("job_settings")
        return typing.cast(typing.Optional["JobSettings"], result)

    @builtins.property
    def stack_capabilities(self) -> typing.Optional[typing.List["StackCapabilities"]]:
        '''In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack.

        If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities``
        error.

        :default: ['CAPABILITY_IAM']
        '''
        result = self._values.get("stack_capabilities")
        return typing.cast(typing.Optional[typing.List["StackCapabilities"]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AddGitHubStageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class AwsCredentials(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.AwsCredentials",
):
    '''Provides AWS credenitals to the pipeline jobs.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="fromGitHubSecrets")
    @builtins.classmethod
    def from_git_hub_secrets(
        cls,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
        session_token: typing.Optional[builtins.str] = None,
    ) -> "AwsCredentialsProvider":
        '''Reference credential secrets to authenticate with AWS.

        This method assumes
        that your credentials will be stored as long-lived GitHub Secrets.

        :param access_key_id: Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: Default: - no session token is used
        '''
        props = GitHubSecretsProviderProps(
            access_key_id=access_key_id,
            secret_access_key=secret_access_key,
            session_token=session_token,
        )

        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "fromGitHubSecrets", [props]))

    @jsii.member(jsii_name="fromOpenIdConnect")
    @builtins.classmethod
    def from_open_id_connect(
        cls,
        *,
        git_hub_action_role_arn: builtins.str,
    ) -> "AwsCredentialsProvider":
        '''Provide AWS credentials using OpenID Connect.

        :param git_hub_action_role_arn: A role that utilizes the GitHub OIDC Identity Provider in your AWS account. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you.
        '''
        props = OpenIdConnectProviderProps(
            git_hub_action_role_arn=git_hub_action_role_arn
        )

        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "fromOpenIdConnect", [props]))

    @jsii.member(jsii_name="runnerHasPreconfiguredCreds")
    @builtins.classmethod
    def runner_has_preconfigured_creds(cls) -> "AwsCredentialsProvider":
        '''Don't provide any AWS credentials, use this if runners have preconfigured credentials.'''
        return typing.cast("AwsCredentialsProvider", jsii.sinvoke(cls, "runnerHasPreconfiguredCreds", []))


class AwsCredentialsProvider(
    metaclass=jsii.JSIIAbstractClass,
    jsii_type="cdk-pipelines-github.AwsCredentialsProvider",
):
    '''AWS credential provider.'''

    def __init__(self) -> None:
        jsii.create(self.__class__, self, [])

    @jsii.member(jsii_name="credentialSteps")
    @abc.abstractmethod
    def credential_steps(
        self,
        region: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
    ) -> typing.List["JobStep"]:
        '''
        :param region: -
        :param assume_role_arn: -
        '''
        ...

    @jsii.member(jsii_name="jobPermission")
    @abc.abstractmethod
    def job_permission(self) -> "JobPermission":
        ...


class _AwsCredentialsProviderProxy(AwsCredentialsProvider):
    @jsii.member(jsii_name="credentialSteps")
    def credential_steps(
        self,
        region: builtins.str,
        assume_role_arn: typing.Optional[builtins.str] = None,
    ) -> typing.List["JobStep"]:
        '''
        :param region: -
        :param assume_role_arn: -
        '''
        if __debug__:
            def stub(
                region: builtins.str,
                assume_role_arn: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument region", value=region, expected_type=type_hints["region"])
            check_type(argname="argument assume_role_arn", value=assume_role_arn, expected_type=type_hints["assume_role_arn"])
        return typing.cast(typing.List["JobStep"], jsii.invoke(self, "credentialSteps", [region, assume_role_arn]))

    @jsii.member(jsii_name="jobPermission")
    def job_permission(self) -> "JobPermission":
        return typing.cast("JobPermission", jsii.invoke(self, "jobPermission", []))

# Adding a "__jsii_proxy_class__(): typing.Type" function to the abstract class
typing.cast(typing.Any, AwsCredentialsProvider).__jsii_proxy_class__ = lambda : _AwsCredentialsProviderProxy


@jsii.data_type(
    jsii_type="cdk-pipelines-github.AwsCredentialsSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
        "session_token": "sessionToken",
    },
)
class AwsCredentialsSecrets:
    def __init__(
        self,
        *,
        access_key_id: typing.Optional[builtins.str] = None,
        secret_access_key: typing.Optional[builtins.str] = None,
        session_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Names of secrets for AWS credentials.

        :param access_key_id: Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: Default: - no session token is used
        '''
        if __debug__:
            def stub(
                *,
                access_key_id: typing.Optional[builtins.str] = None,
                secret_access_key: typing.Optional[builtins.str] = None,
                session_token: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
        self._values: typing.Dict[str, typing.Any] = {}
        if access_key_id is not None:
            self._values["access_key_id"] = access_key_id
        if secret_access_key is not None:
            self._values["secret_access_key"] = secret_access_key
        if session_token is not None:
            self._values["session_token"] = session_token

    @builtins.property
    def access_key_id(self) -> typing.Optional[builtins.str]:
        '''
        :default: "AWS_ACCESS_KEY_ID"
        '''
        result = self._values.get("access_key_id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def secret_access_key(self) -> typing.Optional[builtins.str]:
        '''
        :default: "AWS_SECRET_ACCESS_KEY"
        '''
        result = self._values.get("secret_access_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''
        :default: - no session token is used
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "AwsCredentialsSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CheckRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Check run options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CheckSuiteOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class CheckSuiteOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Check suite options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CheckSuiteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ContainerCredentials",
    jsii_struct_bases=[],
    name_mapping={"password": "password", "username": "username"},
)
class ContainerCredentials:
    def __init__(self, *, password: builtins.str, username: builtins.str) -> None:
        '''Credentials to use to authenticate to Docker registries.

        :param password: The password.
        :param username: The username.
        '''
        if __debug__:
            def stub(*, password: builtins.str, username: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument password", value=password, expected_type=type_hints["password"])
            check_type(argname="argument username", value=username, expected_type=type_hints["username"])
        self._values: typing.Dict[str, typing.Any] = {
            "password": password,
            "username": username,
        }

    @builtins.property
    def password(self) -> builtins.str:
        '''The password.'''
        result = self._values.get("password")
        assert result is not None, "Required property 'password' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username(self) -> builtins.str:
        '''The username.'''
        result = self._values.get("username")
        assert result is not None, "Required property 'username' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerCredentials(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ContainerOptions",
    jsii_struct_bases=[],
    name_mapping={
        "image": "image",
        "credentials": "credentials",
        "env": "env",
        "options": "options",
        "ports": "ports",
        "volumes": "volumes",
    },
)
class ContainerOptions:
    def __init__(
        self,
        *,
        image: builtins.str,
        credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        options: typing.Optional[typing.Sequence[builtins.str]] = None,
        ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
        volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options petaining to container environments.

        :param image: The Docker image to use as the container to run the action. The value can be the Docker Hub image name or a registry name.
        :param credentials: f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password. The credentials are the same values that you would provide to the docker login command.
        :param env: Sets a map of environment variables in the container.
        :param options: Additional Docker container resource options.
        :param ports: Sets an array of ports to expose on the container.
        :param volumes: Sets an array of volumes for the container to use. You can use volumes to share data between services or other steps in a job. You can specify named Docker volumes, anonymous Docker volumes, or bind mounts on the host. To specify a volume, you specify the source and destination path: ``<source>:<destinationPath>``.
        '''
        if isinstance(credentials, dict):
            credentials = ContainerCredentials(**credentials)
        if __debug__:
            def stub(
                *,
                image: builtins.str,
                credentials: typing.Optional[typing.Union[ContainerCredentials, typing.Dict[str, typing.Any]]] = None,
                env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                options: typing.Optional[typing.Sequence[builtins.str]] = None,
                ports: typing.Optional[typing.Sequence[jsii.Number]] = None,
                volumes: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument image", value=image, expected_type=type_hints["image"])
            check_type(argname="argument credentials", value=credentials, expected_type=type_hints["credentials"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument options", value=options, expected_type=type_hints["options"])
            check_type(argname="argument ports", value=ports, expected_type=type_hints["ports"])
            check_type(argname="argument volumes", value=volumes, expected_type=type_hints["volumes"])
        self._values: typing.Dict[str, typing.Any] = {
            "image": image,
        }
        if credentials is not None:
            self._values["credentials"] = credentials
        if env is not None:
            self._values["env"] = env
        if options is not None:
            self._values["options"] = options
        if ports is not None:
            self._values["ports"] = ports
        if volumes is not None:
            self._values["volumes"] = volumes

    @builtins.property
    def image(self) -> builtins.str:
        '''The Docker image to use as the container to run the action.

        The value can
        be the Docker Hub image name or a registry name.
        '''
        result = self._values.get("image")
        assert result is not None, "Required property 'image' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def credentials(self) -> typing.Optional[ContainerCredentials]:
        '''f the image's container registry requires authentication to pull the image, you can use credentials to set a map of the username and password.

        The credentials are the same values that you would provide to the docker
        login command.
        '''
        result = self._values.get("credentials")
        return typing.cast(typing.Optional[ContainerCredentials], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets a map of environment variables in the container.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def options(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Additional Docker container resource options.

        :see: https://docs.docker.com/engine/reference/commandline/create/#options
        '''
        result = self._values.get("options")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def ports(self) -> typing.Optional[typing.List[jsii.Number]]:
        '''Sets an array of ports to expose on the container.'''
        result = self._values.get("ports")
        return typing.cast(typing.Optional[typing.List[jsii.Number]], result)

    @builtins.property
    def volumes(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Sets an array of volumes for the container to use.

        You can use volumes to
        share data between services or other steps in a job. You can specify
        named Docker volumes, anonymous Docker volumes, or bind mounts on the
        host.

        To specify a volume, you specify the source and destination path:
        ``<source>:<destinationPath>``.
        '''
        result = self._values.get("volumes")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ContainerOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CreateOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class CreateOptions:
    def __init__(self) -> None:
        '''The Create event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CreateOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.CronScheduleOptions",
    jsii_struct_bases=[],
    name_mapping={"cron": "cron"},
)
class CronScheduleOptions:
    def __init__(self, *, cron: builtins.str) -> None:
        '''CRON schedule options.

        :param cron: 
        '''
        if __debug__:
            def stub(*, cron: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument cron", value=cron, expected_type=type_hints["cron"])
        self._values: typing.Dict[str, typing.Any] = {
            "cron": cron,
        }

    @builtins.property
    def cron(self) -> builtins.str:
        '''
        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        '''
        result = self._values.get("cron")
        assert result is not None, "Required property 'cron' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "CronScheduleOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DeleteOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeleteOptions:
    def __init__(self) -> None:
        '''The Delete event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeleteOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DeploymentOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentOptions:
    def __init__(self) -> None:
        '''The Deployment event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DeploymentStatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class DeploymentStatusOptions:
    def __init__(self) -> None:
        '''The Deployment status event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DeploymentStatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class DockerCredential(
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.DockerCredential",
):
    '''Represents a credential used to authenticate to a docker registry.

    Uses the official Docker Login GitHub Action to authenticate.

    :see: https://github.com/marketplace/actions/docker-login
    '''

    @jsii.member(jsii_name="customRegistry")
    @builtins.classmethod
    def custom_registry(
        cls,
        registry: builtins.str,
        *,
        password_key: builtins.str,
        username_key: builtins.str,
    ) -> "DockerCredential":
        '''Create a credential for a custom registry.

        This method assumes that you will have long-lived
        GitHub Secrets stored under the usernameKey and passwordKey that will authenticate to the
        registry you provide.

        :param registry: -
        :param password_key: The key of the GitHub Secret containing your registry password.
        :param username_key: The key of the GitHub Secret containing your registry username.

        :see: https://github.com/marketplace/actions/docker-login
        '''
        if __debug__:
            def stub(
                registry: builtins.str,
                *,
                password_key: builtins.str,
                username_key: builtins.str,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        creds = ExternalDockerCredentialSecrets(
            password_key=password_key, username_key=username_key
        )

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "customRegistry", [registry, creds]))

    @jsii.member(jsii_name="dockerHub")
    @builtins.classmethod
    def docker_hub(
        cls,
        *,
        personal_access_token_key: typing.Optional[builtins.str] = None,
        username_key: typing.Optional[builtins.str] = None,
    ) -> "DockerCredential":
        '''Reference credential secrets to authenticate to DockerHub.

        This method assumes
        that your credentials will be stored as long-lived GitHub Secrets under the
        usernameKey and personalAccessTokenKey.

        The default for usernameKey is ``DOCKERHUB_USERNAME``. The default for personalAccessTokenKey
        is ``DOCKERHUB_TOKEN``. If you do not set these values, your credentials should be
        found in your GitHub Secrets under these default keys.

        :param personal_access_token_key: The key of the GitHub Secret containing the DockerHub personal access token. Default: 'DOCKERHUB_TOKEN'
        :param username_key: The key of the GitHub Secret containing the DockerHub username. Default: 'DOCKERHUB_USERNAME'
        '''
        creds = DockerHubCredentialSecrets(
            personal_access_token_key=personal_access_token_key,
            username_key=username_key,
        )

        return typing.cast("DockerCredential", jsii.sinvoke(cls, "dockerHub", [creds]))

    @jsii.member(jsii_name="ecr")
    @builtins.classmethod
    def ecr(cls, registry: builtins.str) -> "DockerCredential":
        '''Create a credential for ECR.

        This method will reuse your AWS credentials to log in to AWS.
        Your AWS credentials are already used to deploy your CDK stacks. It can be supplied via
        GitHub Secrets or using an IAM role that trusts the GitHub OIDC identity provider.

        NOTE - All ECR repositories in the same account and region share a domain name
        (e.g., 0123456789012.dkr.ecr.eu-west-1.amazonaws.com), and can only have one associated
        set of credentials (and DockerCredential). Attempting to associate one set of credentials
        with one ECR repo and another with another ECR repo in the same account and region will
        result in failures when using these credentials in the pipeline.

        :param registry: -
        '''
        if __debug__:
            def stub(registry: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument registry", value=registry, expected_type=type_hints["registry"])
        return typing.cast("DockerCredential", jsii.sinvoke(cls, "ecr", [registry]))

    @builtins.property
    @jsii.member(jsii_name="name")
    def name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "name"))

    @builtins.property
    @jsii.member(jsii_name="passwordKey")
    def password_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "passwordKey"))

    @builtins.property
    @jsii.member(jsii_name="registry")
    def registry(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "registry"))

    @builtins.property
    @jsii.member(jsii_name="usernameKey")
    def username_key(self) -> typing.Optional[builtins.str]:
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "usernameKey"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.DockerHubCredentialSecrets",
    jsii_struct_bases=[],
    name_mapping={
        "personal_access_token_key": "personalAccessTokenKey",
        "username_key": "usernameKey",
    },
)
class DockerHubCredentialSecrets:
    def __init__(
        self,
        *,
        personal_access_token_key: typing.Optional[builtins.str] = None,
        username_key: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Locations of GitHub Secrets used to authenticate to DockerHub.

        :param personal_access_token_key: The key of the GitHub Secret containing the DockerHub personal access token. Default: 'DOCKERHUB_TOKEN'
        :param username_key: The key of the GitHub Secret containing the DockerHub username. Default: 'DOCKERHUB_USERNAME'
        '''
        if __debug__:
            def stub(
                *,
                personal_access_token_key: typing.Optional[builtins.str] = None,
                username_key: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument personal_access_token_key", value=personal_access_token_key, expected_type=type_hints["personal_access_token_key"])
            check_type(argname="argument username_key", value=username_key, expected_type=type_hints["username_key"])
        self._values: typing.Dict[str, typing.Any] = {}
        if personal_access_token_key is not None:
            self._values["personal_access_token_key"] = personal_access_token_key
        if username_key is not None:
            self._values["username_key"] = username_key

    @builtins.property
    def personal_access_token_key(self) -> typing.Optional[builtins.str]:
        '''The key of the GitHub Secret containing the DockerHub personal access token.

        :default: 'DOCKERHUB_TOKEN'
        '''
        result = self._values.get("personal_access_token_key")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def username_key(self) -> typing.Optional[builtins.str]:
        '''The key of the GitHub Secret containing the DockerHub username.

        :default: 'DOCKERHUB_USERNAME'
        '''
        result = self._values.get("username_key")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "DockerHubCredentialSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ExternalDockerCredentialSecrets",
    jsii_struct_bases=[],
    name_mapping={"password_key": "passwordKey", "username_key": "usernameKey"},
)
class ExternalDockerCredentialSecrets:
    def __init__(
        self,
        *,
        password_key: builtins.str,
        username_key: builtins.str,
    ) -> None:
        '''Generic structure to supply the locations of GitHub Secrets used to authenticate to a docker registry.

        :param password_key: The key of the GitHub Secret containing your registry password.
        :param username_key: The key of the GitHub Secret containing your registry username.
        '''
        if __debug__:
            def stub(*, password_key: builtins.str, username_key: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument password_key", value=password_key, expected_type=type_hints["password_key"])
            check_type(argname="argument username_key", value=username_key, expected_type=type_hints["username_key"])
        self._values: typing.Dict[str, typing.Any] = {
            "password_key": password_key,
            "username_key": username_key,
        }

    @builtins.property
    def password_key(self) -> builtins.str:
        '''The key of the GitHub Secret containing your registry password.'''
        result = self._values.get("password_key")
        assert result is not None, "Required property 'password_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def username_key(self) -> builtins.str:
        '''The key of the GitHub Secret containing your registry username.'''
        result = self._values.get("username_key")
        assert result is not None, "Required property 'username_key' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ExternalDockerCredentialSecrets(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ForkOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class ForkOptions:
    def __init__(self) -> None:
        '''The Fork event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ForkOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubActionRole(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubActionRole",
):
    '''Creates or references a GitHub OIDC provider and accompanying role that trusts the provider.

    This role can be used to authenticate against AWS instead of using long-lived AWS user credentials
    stored in GitHub secrets.

    You can do this manually in the console, or create a separate stack that uses this construct.
    You must ``cdk deploy`` once (with your normal AWS credentials) to have this role created for you.

    You can then make note of the role arn in the stack output and send it into the Github Workflow app via
    the ``gitHubActionRoleArn`` property. The role arn will be ``arn:aws:iam::<accountId>:role/GithubActionRole``.

    :see: https://docs.github.com/en/actions/deployment/security-hardening-your-deployments/configuring-openid-connect-in-amazon-web-services
    '''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        repos: typing.Sequence[builtins.str],
        provider: typing.Optional[aws_cdk.aws_iam.IOpenIdConnectProvider] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param repos: A list of GitHub repositories you want to be able to access the IAM role. Each entry should be your GitHub username and repository passed in as a single string. For example, `['owner/repo1', 'owner/repo2'].
        :param provider: The GitHub OpenId Connect Provider. Must have provider url ``https://token.actions.githubusercontent.com``. The audience must be ``sts:amazonaws.com``. Only one such provider can be defined per account, so if you already have a provider with the same url, a new provider cannot be created for you. Default: - a provider is created for you.
        :param role_name: The name of the Oidc role. Default: 'GitHubActionRole'
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                repos: typing.Sequence[builtins.str],
                provider: typing.Optional[aws_cdk.aws_iam.IOpenIdConnectProvider] = None,
                role_name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionRoleProps(
            repos=repos, provider=provider, role_name=role_name
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="existingGitHubActionsProvider")
    @builtins.classmethod
    def existing_git_hub_actions_provider(
        cls,
        scope: constructs.Construct,
    ) -> aws_cdk.aws_iam.IOpenIdConnectProvider:
        '''Reference an existing GitHub Actions provider.

        You do not need to pass in an arn because the arn for such
        a provider is always the same.

        :param scope: -
        '''
        if __debug__:
            def stub(scope: constructs.Construct) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
        return typing.cast(aws_cdk.aws_iam.IOpenIdConnectProvider, jsii.sinvoke(cls, "existingGitHubActionsProvider", [scope]))

    @builtins.property
    @jsii.member(jsii_name="role")
    def role(self) -> aws_cdk.aws_iam.IRole:
        '''The role that gets created.

        You should use the arn of this role as input to the ``gitHubActionRoleArn``
        property in your GitHub Workflow app.
        '''
        return typing.cast(aws_cdk.aws_iam.IRole, jsii.get(self, "role"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubActionRoleProps",
    jsii_struct_bases=[],
    name_mapping={"repos": "repos", "provider": "provider", "role_name": "roleName"},
)
class GitHubActionRoleProps:
    def __init__(
        self,
        *,
        repos: typing.Sequence[builtins.str],
        provider: typing.Optional[aws_cdk.aws_iam.IOpenIdConnectProvider] = None,
        role_name: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Properties for the GitHubActionRole construct.

        :param repos: A list of GitHub repositories you want to be able to access the IAM role. Each entry should be your GitHub username and repository passed in as a single string. For example, `['owner/repo1', 'owner/repo2'].
        :param provider: The GitHub OpenId Connect Provider. Must have provider url ``https://token.actions.githubusercontent.com``. The audience must be ``sts:amazonaws.com``. Only one such provider can be defined per account, so if you already have a provider with the same url, a new provider cannot be created for you. Default: - a provider is created for you.
        :param role_name: The name of the Oidc role. Default: 'GitHubActionRole'
        '''
        if __debug__:
            def stub(
                *,
                repos: typing.Sequence[builtins.str],
                provider: typing.Optional[aws_cdk.aws_iam.IOpenIdConnectProvider] = None,
                role_name: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument repos", value=repos, expected_type=type_hints["repos"])
            check_type(argname="argument provider", value=provider, expected_type=type_hints["provider"])
            check_type(argname="argument role_name", value=role_name, expected_type=type_hints["role_name"])
        self._values: typing.Dict[str, typing.Any] = {
            "repos": repos,
        }
        if provider is not None:
            self._values["provider"] = provider
        if role_name is not None:
            self._values["role_name"] = role_name

    @builtins.property
    def repos(self) -> typing.List[builtins.str]:
        '''A list of GitHub repositories you want to be able to access the IAM role.

        Each entry should be your GitHub username and repository passed in as a
        single string.

        For example, `['owner/repo1', 'owner/repo2'].
        '''
        result = self._values.get("repos")
        assert result is not None, "Required property 'repos' is missing"
        return typing.cast(typing.List[builtins.str], result)

    @builtins.property
    def provider(self) -> typing.Optional[aws_cdk.aws_iam.IOpenIdConnectProvider]:
        '''The GitHub OpenId Connect Provider. Must have provider url ``https://token.actions.githubusercontent.com``. The audience must be ``sts:amazonaws.com``.

        Only one such provider can be defined per account, so if you already
        have a provider with the same url, a new provider cannot be created for you.

        :default: - a provider is created for you.
        '''
        result = self._values.get("provider")
        return typing.cast(typing.Optional[aws_cdk.aws_iam.IOpenIdConnectProvider], result)

    @builtins.property
    def role_name(self) -> typing.Optional[builtins.str]:
        '''The name of the Oidc role.

        :default: 'GitHubActionRole'
        '''
        result = self._values.get("role_name")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionRoleProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubActionStep(
    aws_cdk.pipelines.Step,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubActionStep",
):
    '''Specifies a GitHub Action as a step in the pipeline.'''

    def __init__(
        self,
        id: builtins.str,
        *,
        job_steps: typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]],
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param id: -
        :param job_steps: The Job steps.
        :param env: Environment variables to set.
        '''
        if __debug__:
            def stub(
                id: builtins.str,
                *,
                job_steps: typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]],
                env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubActionStepProps(job_steps=job_steps, env=env)

        jsii.create(self.__class__, self, [id, props])

    @builtins.property
    @jsii.member(jsii_name="env")
    def env(self) -> typing.Mapping[builtins.str, builtins.str]:
        return typing.cast(typing.Mapping[builtins.str, builtins.str], jsii.get(self, "env"))

    @builtins.property
    @jsii.member(jsii_name="jobSteps")
    def job_steps(self) -> typing.List["JobStep"]:
        return typing.cast(typing.List["JobStep"], jsii.get(self, "jobSteps"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubActionStepProps",
    jsii_struct_bases=[],
    name_mapping={"job_steps": "jobSteps", "env": "env"},
)
class GitHubActionStepProps:
    def __init__(
        self,
        *,
        job_steps: typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]],
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
    ) -> None:
        '''
        :param job_steps: The Job steps.
        :param env: Environment variables to set.
        '''
        if __debug__:
            def stub(
                *,
                job_steps: typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]],
                env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument job_steps", value=job_steps, expected_type=type_hints["job_steps"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
        self._values: typing.Dict[str, typing.Any] = {
            "job_steps": job_steps,
        }
        if env is not None:
            self._values["env"] = env

    @builtins.property
    def job_steps(self) -> typing.List["JobStep"]:
        '''The Job steps.'''
        result = self._values.get("job_steps")
        assert result is not None, "Required property 'job_steps' is missing"
        return typing.cast(typing.List["JobStep"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Environment variables to set.'''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubActionStepProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubSecretsProviderProps",
    jsii_struct_bases=[],
    name_mapping={
        "access_key_id": "accessKeyId",
        "secret_access_key": "secretAccessKey",
        "session_token": "sessionToken",
    },
)
class GitHubSecretsProviderProps:
    def __init__(
        self,
        *,
        access_key_id: builtins.str,
        secret_access_key: builtins.str,
        session_token: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Locations of GitHub Secrets used to authenticate to AWS.

        :param access_key_id: Default: "AWS_ACCESS_KEY_ID"
        :param secret_access_key: Default: "AWS_SECRET_ACCESS_KEY"
        :param session_token: Default: - no session token is used
        '''
        if __debug__:
            def stub(
                *,
                access_key_id: builtins.str,
                secret_access_key: builtins.str,
                session_token: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument access_key_id", value=access_key_id, expected_type=type_hints["access_key_id"])
            check_type(argname="argument secret_access_key", value=secret_access_key, expected_type=type_hints["secret_access_key"])
            check_type(argname="argument session_token", value=session_token, expected_type=type_hints["session_token"])
        self._values: typing.Dict[str, typing.Any] = {
            "access_key_id": access_key_id,
            "secret_access_key": secret_access_key,
        }
        if session_token is not None:
            self._values["session_token"] = session_token

    @builtins.property
    def access_key_id(self) -> builtins.str:
        '''
        :default: "AWS_ACCESS_KEY_ID"
        '''
        result = self._values.get("access_key_id")
        assert result is not None, "Required property 'access_key_id' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def secret_access_key(self) -> builtins.str:
        '''
        :default: "AWS_SECRET_ACCESS_KEY"
        '''
        result = self._values.get("secret_access_key")
        assert result is not None, "Required property 'secret_access_key' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def session_token(self) -> typing.Optional[builtins.str]:
        '''
        :default: - no session token is used
        '''
        result = self._values.get("session_token")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubSecretsProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class GitHubWorkflow(
    aws_cdk.pipelines.PipelineBase,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-pipelines-github.GitHubWorkflow",
):
    '''CDK Pipelines for GitHub workflows.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[str, typing.Any]]] = None,
        aws_creds: typing.Optional[AwsCredentialsProvider] = None,
        build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        git_hub_action_role_arn: typing.Optional[builtins.str] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
        pre_synthed: typing.Optional[builtins.bool] = None,
        publish_assets_auth_region: typing.Optional[builtins.str] = None,
        runner: typing.Optional["Runner"] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_path: typing.Optional[builtins.str] = None,
        workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[str, typing.Any]]] = None,
        synth: aws_cdk.pipelines.IFileSetProducer,
    ) -> None:
        '''
        :param scope: -
        :param id: -
        :param aws_credentials: (deprecated) Names of GitHub repository secrets that include AWS credentials for deployment. Default: - ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param aws_creds: Configure provider for AWS credentials used for deployment. Default: - Get AWS credentials from GitHub secrets ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param build_container: Build container options. Default: - GitHub defaults
        :param cdk_cli_version: Version of the CDK CLI to use. Default: - automatic
        :param docker_credentials: The Docker Credentials to use to login. If you set this variable, you will be logged in to docker when you upload Docker Assets.
        :param git_hub_action_role_arn: (deprecated) A role that utilizes the GitHub OIDC Identity Provider in your AWS account. If supplied, this will be used instead of ``awsCredentials``. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you. Default: - GitHub repository secrets are used instead of OpenId Connect role.
        :param job_settings: Job level settings that will be applied to all jobs in the workflow, including synth and asset deploy jobs. Currently the only valid setting is 'if'. You can use this to run jobs only in specific repositories.
        :param post_build_steps: GitHub workflow steps to execute after build. Default: []
        :param pre_build_steps: GitHub workflow steps to execute before build. Default: []
        :param pre_synthed: Indicates if the repository already contains a synthesized ``cdk.out`` directory, in which case we will simply checkout the repo in jobs that require ``cdk.out``. Default: false
        :param publish_assets_auth_region: Will assume the GitHubActionRole in this region when publishing assets. This is NOT the region in which the assets are published. In most cases, you do not have to worry about this property, and can safely ignore it. Default: "us-west-2"
        :param runner: The type of runner to run the job on. The runner can be either a GitHub-hosted runner or a self-hosted runner. Default: Runner.UBUNTU_LATEST
        :param workflow_name: Name of the workflow. Default: "deploy"
        :param workflow_path: File path for the GitHub workflow. Default: ".github/workflows/deploy.yml"
        :param workflow_triggers: GitHub workflow triggers. Default: - By default, workflow is triggered on push to the ``main`` branch and can also be triggered manually (``workflow_dispatch``).
        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[str, typing.Any]]] = None,
                aws_creds: typing.Optional[AwsCredentialsProvider] = None,
                build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]] = None,
                cdk_cli_version: typing.Optional[builtins.str] = None,
                docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
                git_hub_action_role_arn: typing.Optional[builtins.str] = None,
                job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
                post_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
                pre_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
                pre_synthed: typing.Optional[builtins.bool] = None,
                publish_assets_auth_region: typing.Optional[builtins.str] = None,
                runner: typing.Optional["Runner"] = None,
                workflow_name: typing.Optional[builtins.str] = None,
                workflow_path: typing.Optional[builtins.str] = None,
                workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[str, typing.Any]]] = None,
                synth: aws_cdk.pipelines.IFileSetProducer,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = GitHubWorkflowProps(
            aws_credentials=aws_credentials,
            aws_creds=aws_creds,
            build_container=build_container,
            cdk_cli_version=cdk_cli_version,
            docker_credentials=docker_credentials,
            git_hub_action_role_arn=git_hub_action_role_arn,
            job_settings=job_settings,
            post_build_steps=post_build_steps,
            pre_build_steps=pre_build_steps,
            pre_synthed=pre_synthed,
            publish_assets_auth_region=publish_assets_auth_region,
            runner=runner,
            workflow_name=workflow_name,
            workflow_path=workflow_path,
            workflow_triggers=workflow_triggers,
            synth=synth,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @jsii.member(jsii_name="addStageWithGitHubOptions")
    def add_stage_with_git_hub_options(
        self,
        stage: aws_cdk.Stage,
        *,
        git_hub_environment: typing.Optional[builtins.str] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
        stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
        post: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
        pre: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
        stack_steps: typing.Optional[typing.Sequence[typing.Union[aws_cdk.pipelines.StackSteps, typing.Dict[str, typing.Any]]]] = None,
    ) -> aws_cdk.pipelines.StageDeployment:
        '''Deploy a single Stage by itself with options for further GitHub configuration.

        Add a Stage to the pipeline, to be deployed in sequence with other Stages added to the pipeline.
        All Stacks in the stage will be deployed in an order automatically determined by their relative dependencies.

        :param stage: -
        :param git_hub_environment: Run the stage in a specific GitHub Environment. If specified, any protection rules configured for the environment must pass before the job is set to a runner. For example, if the environment has a manual approval rule configured, then the workflow will wait for the approval before sending the job to the runner. Running a workflow that references an environment that does not exist will create an environment with the referenced name. Default: - no GitHub environment
        :param job_settings: Job level settings that will be applied to all jobs in the stage. Currently the only valid setting is 'if'.
        :param stack_capabilities: In some cases, you must explicitly acknowledge that your CloudFormation stack template contains certain capabilities in order for CloudFormation to create the stack. If insufficiently specified, CloudFormation returns an ``InsufficientCapabilities`` error. Default: ['CAPABILITY_IAM']
        :param post: Additional steps to run after all of the stacks in the stage. Default: - No additional steps
        :param pre: Additional steps to run before any of the stacks in the stage. Default: - No additional steps
        :param stack_steps: Instructions for stack level steps. Default: - No additional instructions
        '''
        if __debug__:
            def stub(
                stage: aws_cdk.Stage,
                *,
                git_hub_environment: typing.Optional[builtins.str] = None,
                job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
                stack_capabilities: typing.Optional[typing.Sequence["StackCapabilities"]] = None,
                post: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
                pre: typing.Optional[typing.Sequence[aws_cdk.pipelines.Step]] = None,
                stack_steps: typing.Optional[typing.Sequence[typing.Union[aws_cdk.pipelines.StackSteps, typing.Dict[str, typing.Any]]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument stage", value=stage, expected_type=type_hints["stage"])
        options = AddGitHubStageOptions(
            git_hub_environment=git_hub_environment,
            job_settings=job_settings,
            stack_capabilities=stack_capabilities,
            post=post,
            pre=pre,
            stack_steps=stack_steps,
        )

        return typing.cast(aws_cdk.pipelines.StageDeployment, jsii.invoke(self, "addStageWithGitHubOptions", [stage, options]))

    @jsii.member(jsii_name="doBuildPipeline")
    def _do_build_pipeline(self) -> None:
        '''Implemented by subclasses to do the actual pipeline construction.'''
        return typing.cast(None, jsii.invoke(self, "doBuildPipeline", []))

    @builtins.property
    @jsii.member(jsii_name="workflowFile")
    def workflow_file(self) -> "YamlFile":
        return typing.cast("YamlFile", jsii.get(self, "workflowFile"))

    @builtins.property
    @jsii.member(jsii_name="workflowName")
    def workflow_name(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowName"))

    @builtins.property
    @jsii.member(jsii_name="workflowPath")
    def workflow_path(self) -> builtins.str:
        return typing.cast(builtins.str, jsii.get(self, "workflowPath"))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GitHubWorkflowProps",
    jsii_struct_bases=[aws_cdk.pipelines.PipelineBaseProps],
    name_mapping={
        "synth": "synth",
        "aws_credentials": "awsCredentials",
        "aws_creds": "awsCreds",
        "build_container": "buildContainer",
        "cdk_cli_version": "cdkCliVersion",
        "docker_credentials": "dockerCredentials",
        "git_hub_action_role_arn": "gitHubActionRoleArn",
        "job_settings": "jobSettings",
        "post_build_steps": "postBuildSteps",
        "pre_build_steps": "preBuildSteps",
        "pre_synthed": "preSynthed",
        "publish_assets_auth_region": "publishAssetsAuthRegion",
        "runner": "runner",
        "workflow_name": "workflowName",
        "workflow_path": "workflowPath",
        "workflow_triggers": "workflowTriggers",
    },
)
class GitHubWorkflowProps(aws_cdk.pipelines.PipelineBaseProps):
    def __init__(
        self,
        *,
        synth: aws_cdk.pipelines.IFileSetProducer,
        aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[str, typing.Any]]] = None,
        aws_creds: typing.Optional[AwsCredentialsProvider] = None,
        build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]] = None,
        cdk_cli_version: typing.Optional[builtins.str] = None,
        docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
        git_hub_action_role_arn: typing.Optional[builtins.str] = None,
        job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
        post_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
        pre_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
        pre_synthed: typing.Optional[builtins.bool] = None,
        publish_assets_auth_region: typing.Optional[builtins.str] = None,
        runner: typing.Optional["Runner"] = None,
        workflow_name: typing.Optional[builtins.str] = None,
        workflow_path: typing.Optional[builtins.str] = None,
        workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''Props for ``GitHubWorkflow``.

        :param synth: The build step that produces the CDK Cloud Assembly. The primary output of this step needs to be the ``cdk.out`` directory generated by the ``cdk synth`` command. If you use a ``ShellStep`` here and you don't configure an output directory, the output directory will automatically be assumed to be ``cdk.out``.
        :param aws_credentials: (deprecated) Names of GitHub repository secrets that include AWS credentials for deployment. Default: - ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param aws_creds: Configure provider for AWS credentials used for deployment. Default: - Get AWS credentials from GitHub secrets ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        :param build_container: Build container options. Default: - GitHub defaults
        :param cdk_cli_version: Version of the CDK CLI to use. Default: - automatic
        :param docker_credentials: The Docker Credentials to use to login. If you set this variable, you will be logged in to docker when you upload Docker Assets.
        :param git_hub_action_role_arn: (deprecated) A role that utilizes the GitHub OIDC Identity Provider in your AWS account. If supplied, this will be used instead of ``awsCredentials``. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you. Default: - GitHub repository secrets are used instead of OpenId Connect role.
        :param job_settings: Job level settings that will be applied to all jobs in the workflow, including synth and asset deploy jobs. Currently the only valid setting is 'if'. You can use this to run jobs only in specific repositories.
        :param post_build_steps: GitHub workflow steps to execute after build. Default: []
        :param pre_build_steps: GitHub workflow steps to execute before build. Default: []
        :param pre_synthed: Indicates if the repository already contains a synthesized ``cdk.out`` directory, in which case we will simply checkout the repo in jobs that require ``cdk.out``. Default: false
        :param publish_assets_auth_region: Will assume the GitHubActionRole in this region when publishing assets. This is NOT the region in which the assets are published. In most cases, you do not have to worry about this property, and can safely ignore it. Default: "us-west-2"
        :param runner: The type of runner to run the job on. The runner can be either a GitHub-hosted runner or a self-hosted runner. Default: Runner.UBUNTU_LATEST
        :param workflow_name: Name of the workflow. Default: "deploy"
        :param workflow_path: File path for the GitHub workflow. Default: ".github/workflows/deploy.yml"
        :param workflow_triggers: GitHub workflow triggers. Default: - By default, workflow is triggered on push to the ``main`` branch and can also be triggered manually (``workflow_dispatch``).
        '''
        if isinstance(aws_credentials, dict):
            aws_credentials = AwsCredentialsSecrets(**aws_credentials)
        if isinstance(build_container, dict):
            build_container = ContainerOptions(**build_container)
        if isinstance(job_settings, dict):
            job_settings = JobSettings(**job_settings)
        if isinstance(workflow_triggers, dict):
            workflow_triggers = WorkflowTriggers(**workflow_triggers)
        if __debug__:
            def stub(
                *,
                synth: aws_cdk.pipelines.IFileSetProducer,
                aws_credentials: typing.Optional[typing.Union[AwsCredentialsSecrets, typing.Dict[str, typing.Any]]] = None,
                aws_creds: typing.Optional[AwsCredentialsProvider] = None,
                build_container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]] = None,
                cdk_cli_version: typing.Optional[builtins.str] = None,
                docker_credentials: typing.Optional[typing.Sequence[DockerCredential]] = None,
                git_hub_action_role_arn: typing.Optional[builtins.str] = None,
                job_settings: typing.Optional[typing.Union["JobSettings", typing.Dict[str, typing.Any]]] = None,
                post_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
                pre_build_steps: typing.Optional[typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]]] = None,
                pre_synthed: typing.Optional[builtins.bool] = None,
                publish_assets_auth_region: typing.Optional[builtins.str] = None,
                runner: typing.Optional["Runner"] = None,
                workflow_name: typing.Optional[builtins.str] = None,
                workflow_path: typing.Optional[builtins.str] = None,
                workflow_triggers: typing.Optional[typing.Union["WorkflowTriggers", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument synth", value=synth, expected_type=type_hints["synth"])
            check_type(argname="argument aws_credentials", value=aws_credentials, expected_type=type_hints["aws_credentials"])
            check_type(argname="argument aws_creds", value=aws_creds, expected_type=type_hints["aws_creds"])
            check_type(argname="argument build_container", value=build_container, expected_type=type_hints["build_container"])
            check_type(argname="argument cdk_cli_version", value=cdk_cli_version, expected_type=type_hints["cdk_cli_version"])
            check_type(argname="argument docker_credentials", value=docker_credentials, expected_type=type_hints["docker_credentials"])
            check_type(argname="argument git_hub_action_role_arn", value=git_hub_action_role_arn, expected_type=type_hints["git_hub_action_role_arn"])
            check_type(argname="argument job_settings", value=job_settings, expected_type=type_hints["job_settings"])
            check_type(argname="argument post_build_steps", value=post_build_steps, expected_type=type_hints["post_build_steps"])
            check_type(argname="argument pre_build_steps", value=pre_build_steps, expected_type=type_hints["pre_build_steps"])
            check_type(argname="argument pre_synthed", value=pre_synthed, expected_type=type_hints["pre_synthed"])
            check_type(argname="argument publish_assets_auth_region", value=publish_assets_auth_region, expected_type=type_hints["publish_assets_auth_region"])
            check_type(argname="argument runner", value=runner, expected_type=type_hints["runner"])
            check_type(argname="argument workflow_name", value=workflow_name, expected_type=type_hints["workflow_name"])
            check_type(argname="argument workflow_path", value=workflow_path, expected_type=type_hints["workflow_path"])
            check_type(argname="argument workflow_triggers", value=workflow_triggers, expected_type=type_hints["workflow_triggers"])
        self._values: typing.Dict[str, typing.Any] = {
            "synth": synth,
        }
        if aws_credentials is not None:
            self._values["aws_credentials"] = aws_credentials
        if aws_creds is not None:
            self._values["aws_creds"] = aws_creds
        if build_container is not None:
            self._values["build_container"] = build_container
        if cdk_cli_version is not None:
            self._values["cdk_cli_version"] = cdk_cli_version
        if docker_credentials is not None:
            self._values["docker_credentials"] = docker_credentials
        if git_hub_action_role_arn is not None:
            self._values["git_hub_action_role_arn"] = git_hub_action_role_arn
        if job_settings is not None:
            self._values["job_settings"] = job_settings
        if post_build_steps is not None:
            self._values["post_build_steps"] = post_build_steps
        if pre_build_steps is not None:
            self._values["pre_build_steps"] = pre_build_steps
        if pre_synthed is not None:
            self._values["pre_synthed"] = pre_synthed
        if publish_assets_auth_region is not None:
            self._values["publish_assets_auth_region"] = publish_assets_auth_region
        if runner is not None:
            self._values["runner"] = runner
        if workflow_name is not None:
            self._values["workflow_name"] = workflow_name
        if workflow_path is not None:
            self._values["workflow_path"] = workflow_path
        if workflow_triggers is not None:
            self._values["workflow_triggers"] = workflow_triggers

    @builtins.property
    def synth(self) -> aws_cdk.pipelines.IFileSetProducer:
        '''The build step that produces the CDK Cloud Assembly.

        The primary output of this step needs to be the ``cdk.out`` directory
        generated by the ``cdk synth`` command.

        If you use a ``ShellStep`` here and you don't configure an output directory,
        the output directory will automatically be assumed to be ``cdk.out``.
        '''
        result = self._values.get("synth")
        assert result is not None, "Required property 'synth' is missing"
        return typing.cast(aws_cdk.pipelines.IFileSetProducer, result)

    @builtins.property
    def aws_credentials(self) -> typing.Optional[AwsCredentialsSecrets]:
        '''(deprecated) Names of GitHub repository secrets that include AWS credentials for deployment.

        :default: - ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.

        :deprecated: Use ``awsCreds.fromGitHubSecrets()`` instead.

        :stability: deprecated
        '''
        result = self._values.get("aws_credentials")
        return typing.cast(typing.Optional[AwsCredentialsSecrets], result)

    @builtins.property
    def aws_creds(self) -> typing.Optional[AwsCredentialsProvider]:
        '''Configure provider for AWS credentials used for deployment.

        :default: - Get AWS credentials from GitHub secrets ``AWS_ACCESS_KEY_ID`` and ``AWS_SECRET_ACCESS_KEY``.
        '''
        result = self._values.get("aws_creds")
        return typing.cast(typing.Optional[AwsCredentialsProvider], result)

    @builtins.property
    def build_container(self) -> typing.Optional[ContainerOptions]:
        '''Build container options.

        :default: - GitHub defaults
        '''
        result = self._values.get("build_container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def cdk_cli_version(self) -> typing.Optional[builtins.str]:
        '''Version of the CDK CLI to use.

        :default: - automatic
        '''
        result = self._values.get("cdk_cli_version")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def docker_credentials(self) -> typing.Optional[typing.List[DockerCredential]]:
        '''The Docker Credentials to use to login.

        If you set this variable,
        you will be logged in to docker when you upload Docker Assets.
        '''
        result = self._values.get("docker_credentials")
        return typing.cast(typing.Optional[typing.List[DockerCredential]], result)

    @builtins.property
    def git_hub_action_role_arn(self) -> typing.Optional[builtins.str]:
        '''(deprecated) A role that utilizes the GitHub OIDC Identity Provider in your AWS account.

        If supplied, this will be used instead of ``awsCredentials``.

        You can create your own role in the console with the necessary trust policy
        to allow gitHub actions from your gitHub repository to assume the role, or
        you can utilize the ``GitHubActionRole`` construct to create a role for you.

        :default: - GitHub repository secrets are used instead of OpenId Connect role.

        :deprecated: Use ``awsCreds.fromOpenIdConnect()`` instead.

        :stability: deprecated
        '''
        result = self._values.get("git_hub_action_role_arn")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def job_settings(self) -> typing.Optional["JobSettings"]:
        '''Job level settings that will be applied to all jobs in the workflow, including synth and asset deploy jobs.

        Currently the only valid setting
        is 'if'. You can use this to run jobs only in specific repositories.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#example-only-run-job-for-specific-repository
        '''
        result = self._values.get("job_settings")
        return typing.cast(typing.Optional["JobSettings"], result)

    @builtins.property
    def post_build_steps(self) -> typing.Optional[typing.List["JobStep"]]:
        '''GitHub workflow steps to execute after build.

        :default: []
        '''
        result = self._values.get("post_build_steps")
        return typing.cast(typing.Optional[typing.List["JobStep"]], result)

    @builtins.property
    def pre_build_steps(self) -> typing.Optional[typing.List["JobStep"]]:
        '''GitHub workflow steps to execute before build.

        :default: []
        '''
        result = self._values.get("pre_build_steps")
        return typing.cast(typing.Optional[typing.List["JobStep"]], result)

    @builtins.property
    def pre_synthed(self) -> typing.Optional[builtins.bool]:
        '''Indicates if the repository already contains a synthesized ``cdk.out`` directory, in which case we will simply checkout the repo in jobs that require ``cdk.out``.

        :default: false
        '''
        result = self._values.get("pre_synthed")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def publish_assets_auth_region(self) -> typing.Optional[builtins.str]:
        '''Will assume the GitHubActionRole in this region when publishing assets.

        This is NOT the region in which the assets are published.

        In most cases, you do not have to worry about this property, and can safely
        ignore it.

        :default: "us-west-2"
        '''
        result = self._values.get("publish_assets_auth_region")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def runner(self) -> typing.Optional["Runner"]:
        '''The type of runner to run the job on.

        The runner can be either a
        GitHub-hosted runner or a self-hosted runner.

        :default: Runner.UBUNTU_LATEST
        '''
        result = self._values.get("runner")
        return typing.cast(typing.Optional["Runner"], result)

    @builtins.property
    def workflow_name(self) -> typing.Optional[builtins.str]:
        '''Name of the workflow.

        :default: "deploy"
        '''
        result = self._values.get("workflow_name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_path(self) -> typing.Optional[builtins.str]:
        '''File path for the GitHub workflow.

        :default: ".github/workflows/deploy.yml"
        '''
        result = self._values.get("workflow_path")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def workflow_triggers(self) -> typing.Optional["WorkflowTriggers"]:
        '''GitHub workflow triggers.

        :default:

        - By default, workflow is triggered on push to the ``main`` branch
        and can also be triggered manually (``workflow_dispatch``).
        '''
        result = self._values.get("workflow_triggers")
        return typing.cast(typing.Optional["WorkflowTriggers"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GitHubWorkflowProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.GollumOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class GollumOptions:
    def __init__(self) -> None:
        '''The Gollum event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "GollumOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.IssueCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssueCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Issue comment options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssueCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.IssuesOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class IssuesOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Issues options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "IssuesOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.Job",
    jsii_struct_bases=[],
    name_mapping={
        "permissions": "permissions",
        "runs_on": "runsOn",
        "steps": "steps",
        "concurrency": "concurrency",
        "container": "container",
        "continue_on_error": "continueOnError",
        "defaults": "defaults",
        "env": "env",
        "environment": "environment",
        "if_": "if",
        "name": "name",
        "needs": "needs",
        "outputs": "outputs",
        "services": "services",
        "strategy": "strategy",
        "timeout_minutes": "timeoutMinutes",
    },
)
class Job:
    def __init__(
        self,
        *,
        permissions: typing.Union["JobPermissions", typing.Dict[str, typing.Any]],
        runs_on: typing.Union[builtins.str, typing.Sequence[builtins.str]],
        steps: typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]],
        concurrency: typing.Any = None,
        container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]] = None,
        continue_on_error: typing.Optional[builtins.bool] = None,
        defaults: typing.Optional[typing.Union["JobDefaults", typing.Dict[str, typing.Any]]] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        environment: typing.Any = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        needs: typing.Optional[typing.Sequence[builtins.str]] = None,
        outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]]] = None,
        strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[str, typing.Any]]] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''A GitHub Workflow job definition.

        :param permissions: You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access. Use ``{ contents: READ }`` if your job only needs to clone code. This is intentionally a required field since it is required in order to allow workflows to run in GitHub repositories with restricted default access.
        :param runs_on: The type of machine to run the job on. The machine can be either a GitHub-hosted runner or a self-hosted runner.
        :param steps: A job contains a sequence of tasks called steps. Steps can run commands, run setup tasks, or run an action in your repository, a public repository, or an action published in a Docker registry. Not all steps run actions, but all actions run as a step. Each step runs in its own process in the runner environment and has access to the workspace and filesystem. Because steps run in their own process, changes to environment variables are not preserved between steps. GitHub provides built-in steps to set up and complete a job.
        :param concurrency: (experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time. A concurrency group can be any string or expression. The expression can use any context except for the secrets context.
        :param container: A container to run any steps in a job that don't already specify a container. If you have steps that use both script and container actions, the container actions will run as sibling containers on the same network with the same volume mounts.
        :param continue_on_error: Prevents a workflow run from failing when a job fails. Set to true to allow a workflow run to pass when this job fails.
        :param defaults: A map of default settings that will apply to all steps in the job. You can also set default settings for the entire workflow.
        :param env: A map of environment variables that are available to all steps in the job. You can also set environment variables for the entire workflow or an individual step.
        :param environment: The environment that the job references. All environment protection rules must pass before a job referencing the environment is sent to a runner.
        :param if_: You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: The name of the job displayed on GitHub.
        :param needs: Identifies any jobs that must complete successfully before this job will run. It can be a string or array of strings. If a job fails, all jobs that need it are skipped unless the jobs use a conditional expression that causes the job to continue.
        :param outputs: A map of outputs for a job. Job outputs are available to all downstream jobs that depend on this job.
        :param services: Used to host service containers for a job in a workflow. Service containers are useful for creating databases or cache services like Redis. The runner automatically creates a Docker network and manages the life cycle of the service containers.
        :param strategy: A strategy creates a build matrix for your jobs. You can define different variations to run each job in.
        :param timeout_minutes: The maximum number of minutes to let a job run before GitHub automatically cancels it. Default: 360
        '''
        if isinstance(permissions, dict):
            permissions = JobPermissions(**permissions)
        if isinstance(container, dict):
            container = ContainerOptions(**container)
        if isinstance(defaults, dict):
            defaults = JobDefaults(**defaults)
        if isinstance(strategy, dict):
            strategy = JobStrategy(**strategy)
        if __debug__:
            def stub(
                *,
                permissions: typing.Union["JobPermissions", typing.Dict[str, typing.Any]],
                runs_on: typing.Union[builtins.str, typing.Sequence[builtins.str]],
                steps: typing.Sequence[typing.Union["JobStep", typing.Dict[str, typing.Any]]],
                concurrency: typing.Any = None,
                container: typing.Optional[typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]] = None,
                continue_on_error: typing.Optional[builtins.bool] = None,
                defaults: typing.Optional[typing.Union["JobDefaults", typing.Dict[str, typing.Any]]] = None,
                env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                environment: typing.Any = None,
                if_: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                needs: typing.Optional[typing.Sequence[builtins.str]] = None,
                outputs: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                services: typing.Optional[typing.Mapping[builtins.str, typing.Union[ContainerOptions, typing.Dict[str, typing.Any]]]] = None,
                strategy: typing.Optional[typing.Union["JobStrategy", typing.Dict[str, typing.Any]]] = None,
                timeout_minutes: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument permissions", value=permissions, expected_type=type_hints["permissions"])
            check_type(argname="argument runs_on", value=runs_on, expected_type=type_hints["runs_on"])
            check_type(argname="argument steps", value=steps, expected_type=type_hints["steps"])
            check_type(argname="argument concurrency", value=concurrency, expected_type=type_hints["concurrency"])
            check_type(argname="argument container", value=container, expected_type=type_hints["container"])
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument defaults", value=defaults, expected_type=type_hints["defaults"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument environment", value=environment, expected_type=type_hints["environment"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument needs", value=needs, expected_type=type_hints["needs"])
            check_type(argname="argument outputs", value=outputs, expected_type=type_hints["outputs"])
            check_type(argname="argument services", value=services, expected_type=type_hints["services"])
            check_type(argname="argument strategy", value=strategy, expected_type=type_hints["strategy"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
        self._values: typing.Dict[str, typing.Any] = {
            "permissions": permissions,
            "runs_on": runs_on,
            "steps": steps,
        }
        if concurrency is not None:
            self._values["concurrency"] = concurrency
        if container is not None:
            self._values["container"] = container
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if defaults is not None:
            self._values["defaults"] = defaults
        if env is not None:
            self._values["env"] = env
        if environment is not None:
            self._values["environment"] = environment
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if needs is not None:
            self._values["needs"] = needs
        if outputs is not None:
            self._values["outputs"] = outputs
        if services is not None:
            self._values["services"] = services
        if strategy is not None:
            self._values["strategy"] = strategy
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes

    @builtins.property
    def permissions(self) -> "JobPermissions":
        '''You can modify the default permissions granted to the GITHUB_TOKEN, adding or removing access as required, so that you only allow the minimum required access.

        Use ``{ contents: READ }`` if your job only needs to clone code.

        This is intentionally a required field since it is required in order to
        allow workflows to run in GitHub repositories with restricted default
        access.

        :see: https://docs.github.com/en/actions/reference/authentication-in-a-workflow#permissions-for-the-github_token
        '''
        result = self._values.get("permissions")
        assert result is not None, "Required property 'permissions' is missing"
        return typing.cast("JobPermissions", result)

    @builtins.property
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        '''The type of machine to run the job on.

        The machine can be either a
        GitHub-hosted runner or a self-hosted runner.

        Example::

            ["ubuntu-latest"]
        '''
        result = self._values.get("runs_on")
        assert result is not None, "Required property 'runs_on' is missing"
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], result)

    @builtins.property
    def steps(self) -> typing.List["JobStep"]:
        '''A job contains a sequence of tasks called steps.

        Steps can run commands,
        run setup tasks, or run an action in your repository, a public repository,
        or an action published in a Docker registry. Not all steps run actions,
        but all actions run as a step. Each step runs in its own process in the
        runner environment and has access to the workspace and filesystem.
        Because steps run in their own process, changes to environment variables
        are not preserved between steps. GitHub provides built-in steps to set up
        and complete a job.
        '''
        result = self._values.get("steps")
        assert result is not None, "Required property 'steps' is missing"
        return typing.cast(typing.List["JobStep"], result)

    @builtins.property
    def concurrency(self) -> typing.Any:
        '''(experimental) Concurrency ensures that only a single job or workflow using the same concurrency group will run at a time.

        A concurrency group can be any
        string or expression. The expression can use any context except for the
        secrets context.

        :stability: experimental
        '''
        result = self._values.get("concurrency")
        return typing.cast(typing.Any, result)

    @builtins.property
    def container(self) -> typing.Optional[ContainerOptions]:
        '''A container to run any steps in a job that don't already specify a container.

        If you have steps that use both script and container actions,
        the container actions will run as sibling containers on the same network
        with the same volume mounts.
        '''
        result = self._values.get("container")
        return typing.cast(typing.Optional[ContainerOptions], result)

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''Prevents a workflow run from failing when a job fails.

        Set to true to
        allow a workflow run to pass when this job fails.
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def defaults(self) -> typing.Optional["JobDefaults"]:
        '''A map of default settings that will apply to all steps in the job.

        You
        can also set default settings for the entire workflow.
        '''
        result = self._values.get("defaults")
        return typing.cast(typing.Optional["JobDefaults"], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of environment variables that are available to all steps in the job.

        You can also set environment variables for the entire workflow or an
        individual step.
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def environment(self) -> typing.Any:
        '''The environment that the job references.

        All environment protection rules
        must pass before a job referencing the environment is sent to a runner.

        :see: https://docs.github.com/en/actions/reference/environments
        '''
        result = self._values.get("environment")
        return typing.cast(typing.Any, result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''The name of the job displayed on GitHub.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def needs(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Identifies any jobs that must complete successfully before this job will run.

        It can be a string or array of strings. If a job fails, all jobs
        that need it are skipped unless the jobs use a conditional expression
        that causes the job to continue.
        '''
        result = self._values.get("needs")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def outputs(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''A map of outputs for a job.

        Job outputs are available to all downstream
        jobs that depend on this job.
        '''
        result = self._values.get("outputs")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def services(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, ContainerOptions]]:
        '''Used to host service containers for a job in a workflow.

        Service
        containers are useful for creating databases or cache services like Redis.
        The runner automatically creates a Docker network and manages the life
        cycle of the service containers.
        '''
        result = self._values.get("services")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, ContainerOptions]], result)

    @builtins.property
    def strategy(self) -> typing.Optional["JobStrategy"]:
        '''A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.
        '''
        result = self._values.get("strategy")
        return typing.cast(typing.Optional["JobStrategy"], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of minutes to let a job run before GitHub automatically cancels it.

        :default: 360
        '''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "Job(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobDefaults",
    jsii_struct_bases=[],
    name_mapping={"run": "run"},
)
class JobDefaults:
    def __init__(
        self,
        *,
        run: typing.Optional[typing.Union["RunSettings", typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''Default settings for all steps in the job.

        :param run: Default run settings.
        '''
        if isinstance(run, dict):
            run = RunSettings(**run)
        if __debug__:
            def stub(
                *,
                run: typing.Optional[typing.Union["RunSettings", typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
        self._values: typing.Dict[str, typing.Any] = {}
        if run is not None:
            self._values["run"] = run

    @builtins.property
    def run(self) -> typing.Optional["RunSettings"]:
        '''Default run settings.'''
        result = self._values.get("run")
        return typing.cast(typing.Optional["RunSettings"], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobDefaults(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobMatrix",
    jsii_struct_bases=[],
    name_mapping={"domain": "domain", "exclude": "exclude", "include": "include"},
)
class JobMatrix:
    def __init__(
        self,
        *,
        domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
        exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
        include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
    ) -> None:
        '''A job matrix.

        :param domain: Each option you define in the matrix has a key and value. The keys you define become properties in the matrix context and you can reference the property in other areas of your workflow file. For example, if you define the key os that contains an array of operating systems, you can use the matrix.os property as the value of the runs-on keyword to create a job for each operating system.
        :param exclude: You can remove a specific configurations defined in the build matrix using the exclude option. Using exclude removes a job defined by the build matrix.
        :param include: You can add additional configuration options to a build matrix job that already exists. For example, if you want to use a specific version of npm when the job that uses windows-latest and version 8 of node runs, you can use include to specify that additional option.
        '''
        if __debug__:
            def stub(
                *,
                domain: typing.Optional[typing.Mapping[builtins.str, typing.Sequence[builtins.str]]] = None,
                exclude: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
                include: typing.Optional[typing.Sequence[typing.Mapping[builtins.str, builtins.str]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument domain", value=domain, expected_type=type_hints["domain"])
            check_type(argname="argument exclude", value=exclude, expected_type=type_hints["exclude"])
            check_type(argname="argument include", value=include, expected_type=type_hints["include"])
        self._values: typing.Dict[str, typing.Any] = {}
        if domain is not None:
            self._values["domain"] = domain
        if exclude is not None:
            self._values["exclude"] = exclude
        if include is not None:
            self._values["include"] = include

    @builtins.property
    def domain(
        self,
    ) -> typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]]:
        '''Each option you define in the matrix has a key and value.

        The keys you
        define become properties in the matrix context and you can reference the
        property in other areas of your workflow file. For example, if you define
        the key os that contains an array of operating systems, you can use the
        matrix.os property as the value of the runs-on keyword to create a job
        for each operating system.
        '''
        result = self._values.get("domain")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.List[builtins.str]]], result)

    @builtins.property
    def exclude(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''You can remove a specific configurations defined in the build matrix using the exclude option.

        Using exclude removes a job defined by the
        build matrix.
        '''
        result = self._values.get("exclude")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    @builtins.property
    def include(
        self,
    ) -> typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]]:
        '''You can add additional configuration options to a build matrix job that already exists.

        For example, if you want to use a specific version of npm
        when the job that uses windows-latest and version 8 of node runs, you can
        use include to specify that additional option.
        '''
        result = self._values.get("include")
        return typing.cast(typing.Optional[typing.List[typing.Mapping[builtins.str, builtins.str]]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobMatrix(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.enum(jsii_type="cdk-pipelines-github.JobPermission")
class JobPermission(enum.Enum):
    '''Access level for workflow permission scopes.'''

    READ = "READ"
    '''Read-only access.'''
    WRITE = "WRITE"
    '''Read-write access.'''
    NONE = "NONE"
    '''No access at all.'''


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobPermissions",
    jsii_struct_bases=[],
    name_mapping={
        "actions": "actions",
        "checks": "checks",
        "contents": "contents",
        "deployments": "deployments",
        "discussions": "discussions",
        "id_token": "idToken",
        "issues": "issues",
        "packages": "packages",
        "pull_requests": "pullRequests",
        "repository_projects": "repositoryProjects",
        "security_events": "securityEvents",
        "statuses": "statuses",
    },
)
class JobPermissions:
    def __init__(
        self,
        *,
        actions: typing.Optional[JobPermission] = None,
        checks: typing.Optional[JobPermission] = None,
        contents: typing.Optional[JobPermission] = None,
        deployments: typing.Optional[JobPermission] = None,
        discussions: typing.Optional[JobPermission] = None,
        id_token: typing.Optional[JobPermission] = None,
        issues: typing.Optional[JobPermission] = None,
        packages: typing.Optional[JobPermission] = None,
        pull_requests: typing.Optional[JobPermission] = None,
        repository_projects: typing.Optional[JobPermission] = None,
        security_events: typing.Optional[JobPermission] = None,
        statuses: typing.Optional[JobPermission] = None,
    ) -> None:
        '''The available scopes and access values for workflow permissions.

        If you
        specify the access for any of these scopes, all those that are not
        specified are set to ``JobPermission.NONE``, instead of the default behavior
        when none is specified.

        :param actions: 
        :param checks: 
        :param contents: 
        :param deployments: 
        :param discussions: 
        :param id_token: 
        :param issues: 
        :param packages: 
        :param pull_requests: 
        :param repository_projects: 
        :param security_events: 
        :param statuses: 
        '''
        if __debug__:
            def stub(
                *,
                actions: typing.Optional[JobPermission] = None,
                checks: typing.Optional[JobPermission] = None,
                contents: typing.Optional[JobPermission] = None,
                deployments: typing.Optional[JobPermission] = None,
                discussions: typing.Optional[JobPermission] = None,
                id_token: typing.Optional[JobPermission] = None,
                issues: typing.Optional[JobPermission] = None,
                packages: typing.Optional[JobPermission] = None,
                pull_requests: typing.Optional[JobPermission] = None,
                repository_projects: typing.Optional[JobPermission] = None,
                security_events: typing.Optional[JobPermission] = None,
                statuses: typing.Optional[JobPermission] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument actions", value=actions, expected_type=type_hints["actions"])
            check_type(argname="argument checks", value=checks, expected_type=type_hints["checks"])
            check_type(argname="argument contents", value=contents, expected_type=type_hints["contents"])
            check_type(argname="argument deployments", value=deployments, expected_type=type_hints["deployments"])
            check_type(argname="argument discussions", value=discussions, expected_type=type_hints["discussions"])
            check_type(argname="argument id_token", value=id_token, expected_type=type_hints["id_token"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument packages", value=packages, expected_type=type_hints["packages"])
            check_type(argname="argument pull_requests", value=pull_requests, expected_type=type_hints["pull_requests"])
            check_type(argname="argument repository_projects", value=repository_projects, expected_type=type_hints["repository_projects"])
            check_type(argname="argument security_events", value=security_events, expected_type=type_hints["security_events"])
            check_type(argname="argument statuses", value=statuses, expected_type=type_hints["statuses"])
        self._values: typing.Dict[str, typing.Any] = {}
        if actions is not None:
            self._values["actions"] = actions
        if checks is not None:
            self._values["checks"] = checks
        if contents is not None:
            self._values["contents"] = contents
        if deployments is not None:
            self._values["deployments"] = deployments
        if discussions is not None:
            self._values["discussions"] = discussions
        if id_token is not None:
            self._values["id_token"] = id_token
        if issues is not None:
            self._values["issues"] = issues
        if packages is not None:
            self._values["packages"] = packages
        if pull_requests is not None:
            self._values["pull_requests"] = pull_requests
        if repository_projects is not None:
            self._values["repository_projects"] = repository_projects
        if security_events is not None:
            self._values["security_events"] = security_events
        if statuses is not None:
            self._values["statuses"] = statuses

    @builtins.property
    def actions(self) -> typing.Optional[JobPermission]:
        result = self._values.get("actions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def checks(self) -> typing.Optional[JobPermission]:
        result = self._values.get("checks")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def contents(self) -> typing.Optional[JobPermission]:
        result = self._values.get("contents")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def deployments(self) -> typing.Optional[JobPermission]:
        result = self._values.get("deployments")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def discussions(self) -> typing.Optional[JobPermission]:
        result = self._values.get("discussions")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def id_token(self) -> typing.Optional[JobPermission]:
        result = self._values.get("id_token")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def issues(self) -> typing.Optional[JobPermission]:
        result = self._values.get("issues")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def packages(self) -> typing.Optional[JobPermission]:
        result = self._values.get("packages")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def pull_requests(self) -> typing.Optional[JobPermission]:
        result = self._values.get("pull_requests")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def repository_projects(self) -> typing.Optional[JobPermission]:
        result = self._values.get("repository_projects")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def security_events(self) -> typing.Optional[JobPermission]:
        result = self._values.get("security_events")
        return typing.cast(typing.Optional[JobPermission], result)

    @builtins.property
    def statuses(self) -> typing.Optional[JobPermission]:
        result = self._values.get("statuses")
        return typing.cast(typing.Optional[JobPermission], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobPermissions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobSettings",
    jsii_struct_bases=[],
    name_mapping={"if_": "if"},
)
class JobSettings:
    def __init__(self, *, if_: typing.Optional[builtins.str] = None) -> None:
        '''Job level settings applied to all jobs in the workflow.

        :param if_: jobs.<job_id>.if.
        '''
        if __debug__:
            def stub(*, if_: typing.Optional[builtins.str] = None) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
        self._values: typing.Dict[str, typing.Any] = {}
        if if_ is not None:
            self._values["if_"] = if_

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''jobs.<job_id>.if.

        :see: https://docs.github.com/en/actions/using-workflows/workflow-syntax-for-github-actions#jobsjob_idif
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobStep",
    jsii_struct_bases=[],
    name_mapping={
        "continue_on_error": "continueOnError",
        "env": "env",
        "id": "id",
        "if_": "if",
        "name": "name",
        "run": "run",
        "timeout_minutes": "timeoutMinutes",
        "uses": "uses",
        "with_": "with",
    },
)
class JobStep:
    def __init__(
        self,
        *,
        continue_on_error: typing.Optional[builtins.bool] = None,
        env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
        id: typing.Optional[builtins.str] = None,
        if_: typing.Optional[builtins.str] = None,
        name: typing.Optional[builtins.str] = None,
        run: typing.Optional[builtins.str] = None,
        timeout_minutes: typing.Optional[jsii.Number] = None,
        uses: typing.Optional[builtins.str] = None,
        with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
    ) -> None:
        '''A job step.

        :param continue_on_error: Prevents a job from failing when a step fails. Set to true to allow a job to pass when this step fails.
        :param env: Sets environment variables for steps to use in the runner environment. You can also set environment variables for the entire workflow or a job.
        :param id: A unique identifier for the step. You can use the id to reference the step in contexts.
        :param if_: You can use the if conditional to prevent a job from running unless a condition is met. You can use any supported context and expression to create a conditional.
        :param name: A name for your step to display on GitHub.
        :param run: Runs command-line programs using the operating system's shell. If you do not provide a name, the step name will default to the text specified in the run command.
        :param timeout_minutes: The maximum number of minutes to run the step before killing the process.
        :param uses: Selects an action to run as part of a step in your job. An action is a reusable unit of code. You can use an action defined in the same repository as the workflow, a public repository, or in a published Docker container image.
        :param with_: A map of the input parameters defined by the action. Each input parameter is a key/value pair. Input parameters are set as environment variables. The variable is prefixed with INPUT_ and converted to upper case.
        '''
        if __debug__:
            def stub(
                *,
                continue_on_error: typing.Optional[builtins.bool] = None,
                env: typing.Optional[typing.Mapping[builtins.str, builtins.str]] = None,
                id: typing.Optional[builtins.str] = None,
                if_: typing.Optional[builtins.str] = None,
                name: typing.Optional[builtins.str] = None,
                run: typing.Optional[builtins.str] = None,
                timeout_minutes: typing.Optional[jsii.Number] = None,
                uses: typing.Optional[builtins.str] = None,
                with_: typing.Optional[typing.Mapping[builtins.str, typing.Any]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument continue_on_error", value=continue_on_error, expected_type=type_hints["continue_on_error"])
            check_type(argname="argument env", value=env, expected_type=type_hints["env"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
            check_type(argname="argument if_", value=if_, expected_type=type_hints["if_"])
            check_type(argname="argument name", value=name, expected_type=type_hints["name"])
            check_type(argname="argument run", value=run, expected_type=type_hints["run"])
            check_type(argname="argument timeout_minutes", value=timeout_minutes, expected_type=type_hints["timeout_minutes"])
            check_type(argname="argument uses", value=uses, expected_type=type_hints["uses"])
            check_type(argname="argument with_", value=with_, expected_type=type_hints["with_"])
        self._values: typing.Dict[str, typing.Any] = {}
        if continue_on_error is not None:
            self._values["continue_on_error"] = continue_on_error
        if env is not None:
            self._values["env"] = env
        if id is not None:
            self._values["id"] = id
        if if_ is not None:
            self._values["if_"] = if_
        if name is not None:
            self._values["name"] = name
        if run is not None:
            self._values["run"] = run
        if timeout_minutes is not None:
            self._values["timeout_minutes"] = timeout_minutes
        if uses is not None:
            self._values["uses"] = uses
        if with_ is not None:
            self._values["with_"] = with_

    @builtins.property
    def continue_on_error(self) -> typing.Optional[builtins.bool]:
        '''Prevents a job from failing when a step fails.

        Set to true to allow a job
        to pass when this step fails.
        '''
        result = self._values.get("continue_on_error")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def env(self) -> typing.Optional[typing.Mapping[builtins.str, builtins.str]]:
        '''Sets environment variables for steps to use in the runner environment.

        You can also set environment variables for the entire workflow or a job.
        '''
        result = self._values.get("env")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, builtins.str]], result)

    @builtins.property
    def id(self) -> typing.Optional[builtins.str]:
        '''A unique identifier for the step.

        You can use the id to reference the
        step in contexts.
        '''
        result = self._values.get("id")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def if_(self) -> typing.Optional[builtins.str]:
        '''You can use the if conditional to prevent a job from running unless a condition is met.

        You can use any supported context and expression to
        create a conditional.
        '''
        result = self._values.get("if_")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def name(self) -> typing.Optional[builtins.str]:
        '''A name for your step to display on GitHub.'''
        result = self._values.get("name")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def run(self) -> typing.Optional[builtins.str]:
        '''Runs command-line programs using the operating system's shell.

        If you do
        not provide a name, the step name will default to the text specified in
        the run command.
        '''
        result = self._values.get("run")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def timeout_minutes(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of minutes to run the step before killing the process.'''
        result = self._values.get("timeout_minutes")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def uses(self) -> typing.Optional[builtins.str]:
        '''Selects an action to run as part of a step in your job.

        An action is a
        reusable unit of code. You can use an action defined in the same
        repository as the workflow, a public repository, or in a published Docker
        container image.
        '''
        result = self._values.get("uses")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def with_(self) -> typing.Optional[typing.Mapping[builtins.str, typing.Any]]:
        '''A map of the input parameters defined by the action.

        Each input parameter
        is a key/value pair. Input parameters are set as environment variables.
        The variable is prefixed with INPUT_ and converted to upper case.
        '''
        result = self._values.get("with_")
        return typing.cast(typing.Optional[typing.Mapping[builtins.str, typing.Any]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStep(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobStepOutput",
    jsii_struct_bases=[],
    name_mapping={"output_name": "outputName", "step_id": "stepId"},
)
class JobStepOutput:
    def __init__(self, *, output_name: builtins.str, step_id: builtins.str) -> None:
        '''An output binding for a job.

        :param output_name: The name of the job output that is being bound.
        :param step_id: The ID of the step that exposes the output.
        '''
        if __debug__:
            def stub(*, output_name: builtins.str, step_id: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument output_name", value=output_name, expected_type=type_hints["output_name"])
            check_type(argname="argument step_id", value=step_id, expected_type=type_hints["step_id"])
        self._values: typing.Dict[str, typing.Any] = {
            "output_name": output_name,
            "step_id": step_id,
        }

    @builtins.property
    def output_name(self) -> builtins.str:
        '''The name of the job output that is being bound.'''
        result = self._values.get("output_name")
        assert result is not None, "Required property 'output_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def step_id(self) -> builtins.str:
        '''The ID of the step that exposes the output.'''
        result = self._values.get("step_id")
        assert result is not None, "Required property 'step_id' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStepOutput(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.JobStrategy",
    jsii_struct_bases=[],
    name_mapping={
        "fail_fast": "failFast",
        "matrix": "matrix",
        "max_parallel": "maxParallel",
    },
)
class JobStrategy:
    def __init__(
        self,
        *,
        fail_fast: typing.Optional[builtins.bool] = None,
        matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[str, typing.Any]]] = None,
        max_parallel: typing.Optional[jsii.Number] = None,
    ) -> None:
        '''A strategy creates a build matrix for your jobs.

        You can define different
        variations to run each job in.

        :param fail_fast: When set to true, GitHub cancels all in-progress jobs if any matrix job fails. Default: true
        :param matrix: You can define a matrix of different job configurations. A matrix allows you to create multiple jobs by performing variable substitution in a single job definition. For example, you can use a matrix to create jobs for more than one supported version of a programming language, operating system, or tool. A matrix reuses the job's configuration and creates a job for each matrix you configure. A job matrix can generate a maximum of 256 jobs per workflow run. This limit also applies to self-hosted runners.
        :param max_parallel: The maximum number of jobs that can run simultaneously when using a matrix job strategy. By default, GitHub will maximize the number of jobs run in parallel depending on the available runners on GitHub-hosted virtual machines.
        '''
        if isinstance(matrix, dict):
            matrix = JobMatrix(**matrix)
        if __debug__:
            def stub(
                *,
                fail_fast: typing.Optional[builtins.bool] = None,
                matrix: typing.Optional[typing.Union[JobMatrix, typing.Dict[str, typing.Any]]] = None,
                max_parallel: typing.Optional[jsii.Number] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument fail_fast", value=fail_fast, expected_type=type_hints["fail_fast"])
            check_type(argname="argument matrix", value=matrix, expected_type=type_hints["matrix"])
            check_type(argname="argument max_parallel", value=max_parallel, expected_type=type_hints["max_parallel"])
        self._values: typing.Dict[str, typing.Any] = {}
        if fail_fast is not None:
            self._values["fail_fast"] = fail_fast
        if matrix is not None:
            self._values["matrix"] = matrix
        if max_parallel is not None:
            self._values["max_parallel"] = max_parallel

    @builtins.property
    def fail_fast(self) -> typing.Optional[builtins.bool]:
        '''When set to true, GitHub cancels all in-progress jobs if any matrix job fails.

        Default: true
        '''
        result = self._values.get("fail_fast")
        return typing.cast(typing.Optional[builtins.bool], result)

    @builtins.property
    def matrix(self) -> typing.Optional[JobMatrix]:
        '''You can define a matrix of different job configurations.

        A matrix allows
        you to create multiple jobs by performing variable substitution in a
        single job definition. For example, you can use a matrix to create jobs
        for more than one supported version of a programming language, operating
        system, or tool. A matrix reuses the job's configuration and creates a
        job for each matrix you configure.

        A job matrix can generate a maximum of 256 jobs per workflow run. This
        limit also applies to self-hosted runners.
        '''
        result = self._values.get("matrix")
        return typing.cast(typing.Optional[JobMatrix], result)

    @builtins.property
    def max_parallel(self) -> typing.Optional[jsii.Number]:
        '''The maximum number of jobs that can run simultaneously when using a matrix job strategy.

        By default, GitHub will maximize the number of jobs
        run in parallel depending on the available runners on GitHub-hosted
        virtual machines.
        '''
        result = self._values.get("max_parallel")
        return typing.cast(typing.Optional[jsii.Number], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "JobStrategy(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class JsonPatch(metaclass=jsii.JSIIMeta, jsii_type="cdk-pipelines-github.JsonPatch"):
    '''Utility for applying RFC-6902 JSON-Patch to a document.

    Use the the ``JsonPatch.apply(doc, ...ops)`` function to apply a set of
    operations to a JSON document and return the result.

    Operations can be created using the factory methods ``JsonPatch.add()``,
    ``JsonPatch.remove()``, etc.

    Example::

        const output = JsonPatch.apply(input,
         JsonPatch.replace('/world/hi/there', 'goodbye'),
         JsonPatch.add('/world/foo/', 'boom'),
         JsonPatch.remove('/hello'));
    '''

    @jsii.member(jsii_name="add")
    @builtins.classmethod
    def add(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''Adds a value to an object or inserts it into an array.

        In the case of an
        array, the value is inserted before the given index. The - character can be
        used instead of an index to insert at the end of an array.

        :param path: -
        :param value: -

        Example::

            JsonPatch.add('/biscuits/1', { "name": "Ginger Nut" })
        '''
        if __debug__:
            def stub(path: builtins.str, value: typing.Any) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "add", [path, value]))

    @jsii.member(jsii_name="apply")
    @builtins.classmethod
    def apply(cls, document: typing.Any, *ops: "JsonPatch") -> typing.Any:
        '''Applies a set of JSON-Patch (RFC-6902) operations to ``document`` and returns the result.

        :param document: The document to patch.
        :param ops: The operations to apply.

        :return: The result document
        '''
        if __debug__:
            def stub(document: typing.Any, *ops: "JsonPatch") -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument document", value=document, expected_type=type_hints["document"])
            check_type(argname="argument ops", value=ops, expected_type=typing.Tuple[type_hints["ops"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(typing.Any, jsii.sinvoke(cls, "apply", [document, *ops]))

    @jsii.member(jsii_name="copy")
    @builtins.classmethod
    def copy(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''Copies a value from one location to another within the JSON document.

        Both
        from and path are JSON Pointers.

        :param from_: -
        :param path: -

        Example::

            JsonPatch.copy('/biscuits/0', '/best_biscuit')
        '''
        if __debug__:
            def stub(from_: builtins.str, path: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "copy", [from_, path]))

    @jsii.member(jsii_name="move")
    @builtins.classmethod
    def move(cls, from_: builtins.str, path: builtins.str) -> "JsonPatch":
        '''Moves a value from one location to the other.

        Both from and path are JSON Pointers.

        :param from_: -
        :param path: -

        Example::

            JsonPatch.move('/biscuits', '/cookies')
        '''
        if __debug__:
            def stub(from_: builtins.str, path: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument from_", value=from_, expected_type=type_hints["from_"])
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "move", [from_, path]))

    @jsii.member(jsii_name="remove")
    @builtins.classmethod
    def remove(cls, path: builtins.str) -> "JsonPatch":
        '''Removes a value from an object or array.

        :param path: -

        Example::

            JsonPatch.remove('/biscuits/0')
        '''
        if __debug__:
            def stub(path: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "remove", [path]))

    @jsii.member(jsii_name="replace")
    @builtins.classmethod
    def replace(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''Replaces a value.

        Equivalent to a “remove” followed by an “add”.

        :param path: -
        :param value: -

        Example::

            JsonPatch.replace('/biscuits/0/name', 'Chocolate Digestive')
        '''
        if __debug__:
            def stub(path: builtins.str, value: typing.Any) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "replace", [path, value]))

    @jsii.member(jsii_name="test")
    @builtins.classmethod
    def test(cls, path: builtins.str, value: typing.Any) -> "JsonPatch":
        '''Tests that the specified value is set in the document.

        If the test fails,
        then the patch as a whole should not apply.

        :param path: -
        :param value: -

        Example::

            JsonPatch.test('/best_biscuit/name', 'Choco Leibniz')
        '''
        if __debug__:
            def stub(path: builtins.str, value: typing.Any) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument path", value=path, expected_type=type_hints["path"])
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        return typing.cast("JsonPatch", jsii.sinvoke(cls, "test", [path, value]))


@jsii.data_type(
    jsii_type="cdk-pipelines-github.LabelOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class LabelOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''label options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "LabelOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.MilestoneOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class MilestoneOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Milestone options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "MilestoneOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.OpenIdConnectProviderProps",
    jsii_struct_bases=[],
    name_mapping={"git_hub_action_role_arn": "gitHubActionRoleArn"},
)
class OpenIdConnectProviderProps:
    def __init__(self, *, git_hub_action_role_arn: builtins.str) -> None:
        '''Role to assume using OpenId Connect.

        :param git_hub_action_role_arn: A role that utilizes the GitHub OIDC Identity Provider in your AWS account. You can create your own role in the console with the necessary trust policy to allow gitHub actions from your gitHub repository to assume the role, or you can utilize the ``GitHubActionRole`` construct to create a role for you.
        '''
        if __debug__:
            def stub(*, git_hub_action_role_arn: builtins.str) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument git_hub_action_role_arn", value=git_hub_action_role_arn, expected_type=type_hints["git_hub_action_role_arn"])
        self._values: typing.Dict[str, typing.Any] = {
            "git_hub_action_role_arn": git_hub_action_role_arn,
        }

    @builtins.property
    def git_hub_action_role_arn(self) -> builtins.str:
        '''A role that utilizes the GitHub OIDC Identity Provider in your AWS account.

        You can create your own role in the console with the necessary trust policy
        to allow gitHub actions from your gitHub repository to assume the role, or
        you can utilize the ``GitHubActionRole`` construct to create a role for you.
        '''
        result = self._values.get("git_hub_action_role_arn")
        assert result is not None, "Required property 'git_hub_action_role_arn' is missing"
        return typing.cast(builtins.str, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "OpenIdConnectProviderProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PageBuildOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PageBuildOptions:
    def __init__(self) -> None:
        '''The Page build event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PageBuildOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ProjectCardOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectCardOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Project card options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectCardOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ProjectColumnOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectColumnOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Probject column options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectColumnOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ProjectOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ProjectOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Project options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ProjectOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PublicOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class PublicOptions:
    def __init__(self) -> None:
        '''The Public event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PublicOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestReviewCommentOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewCommentOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request review comment options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewCommentOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestReviewOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class PullRequestReviewOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request review options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestReviewOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PushOptions",
    jsii_struct_bases=[],
    name_mapping={"branches": "branches", "paths": "paths", "tags": "tags"},
)
class PushOptions:
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Options for push-like events.

        :param branches: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        '''
        if __debug__:
            def stub(
                *,
                branches: typing.Optional[typing.Sequence[builtins.str]] = None,
                paths: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
        self._values: typing.Dict[str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PushOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.RegistryPackageOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RegistryPackageOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Registry package options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RegistryPackageOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.ReleaseOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class ReleaseOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Release options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "ReleaseOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.RepositoryDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class RepositoryDispatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Repository dispatch options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RepositoryDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.RunSettings",
    jsii_struct_bases=[],
    name_mapping={"shell": "shell", "working_directory": "workingDirectory"},
)
class RunSettings:
    def __init__(
        self,
        *,
        shell: typing.Optional[builtins.str] = None,
        working_directory: typing.Optional[builtins.str] = None,
    ) -> None:
        '''Run settings for a job.

        :param shell: Which shell to use for running the step.
        :param working_directory: Working directory to use when running the step.
        '''
        if __debug__:
            def stub(
                *,
                shell: typing.Optional[builtins.str] = None,
                working_directory: typing.Optional[builtins.str] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument shell", value=shell, expected_type=type_hints["shell"])
            check_type(argname="argument working_directory", value=working_directory, expected_type=type_hints["working_directory"])
        self._values: typing.Dict[str, typing.Any] = {}
        if shell is not None:
            self._values["shell"] = shell
        if working_directory is not None:
            self._values["working_directory"] = working_directory

    @builtins.property
    def shell(self) -> typing.Optional[builtins.str]:
        '''Which shell to use for running the step.

        Example::

            "bash"
        '''
        result = self._values.get("shell")
        return typing.cast(typing.Optional[builtins.str], result)

    @builtins.property
    def working_directory(self) -> typing.Optional[builtins.str]:
        '''Working directory to use when running the step.'''
        result = self._values.get("working_directory")
        return typing.cast(typing.Optional[builtins.str], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "RunSettings(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class Runner(metaclass=jsii.JSIIMeta, jsii_type="cdk-pipelines-github.Runner"):
    '''The type of runner to run the job on.

    Can be GitHub or Self-hosted.
    In case of self-hosted, a list of labels can be supplied.
    '''

    @jsii.member(jsii_name="selfHosted")
    @builtins.classmethod
    def self_hosted(cls, labels: typing.Sequence[builtins.str]) -> "Runner":
        '''Creates a runner instance that sets runsOn to ``self-hosted``.

        Additional labels can be supplied. There is no need to supply ``self-hosted`` as a label explicitly.

        :param labels: -
        '''
        if __debug__:
            def stub(labels: typing.Sequence[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument labels", value=labels, expected_type=type_hints["labels"])
        return typing.cast("Runner", jsii.sinvoke(cls, "selfHosted", [labels]))

    @jsii.python.classproperty
    @jsii.member(jsii_name="MACOS_LATEST")
    def MACOS_LATEST(cls) -> "Runner":
        '''Runner instance that sets runsOn to ``macos-latest``.'''
        return typing.cast("Runner", jsii.sget(cls, "MACOS_LATEST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="UBUNTU_LATEST")
    def UBUNTU_LATEST(cls) -> "Runner":
        '''Runner instance that sets runsOn to ``ubuntu-latest``.'''
        return typing.cast("Runner", jsii.sget(cls, "UBUNTU_LATEST"))

    @jsii.python.classproperty
    @jsii.member(jsii_name="WINDOWS_LATEST")
    def WINDOWS_LATEST(cls) -> "Runner":
        '''Runner instance that sets runsOn to ``windows-latest``.'''
        return typing.cast("Runner", jsii.sget(cls, "WINDOWS_LATEST"))

    @builtins.property
    @jsii.member(jsii_name="runsOn")
    def runs_on(self) -> typing.Union[builtins.str, typing.List[builtins.str]]:
        return typing.cast(typing.Union[builtins.str, typing.List[builtins.str]], jsii.get(self, "runsOn"))


@jsii.enum(jsii_type="cdk-pipelines-github.StackCapabilities")
class StackCapabilities(enum.Enum):
    '''Acknowledge IAM resources in AWS CloudFormation templates.

    :see: https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/using-iam-template.html#capabilities
    '''

    IAM = "IAM"
    '''Acknowledge your stack includes IAM resources.'''
    NAMED_IAM = "NAMED_IAM"
    '''Acknowledge your stack includes custom names for IAM resources.'''
    AUTO_EXPAND = "AUTO_EXPAND"
    '''Acknowledge your stack contains one or more macros.'''


@jsii.data_type(
    jsii_type="cdk-pipelines-github.StatusOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class StatusOptions:
    def __init__(self) -> None:
        '''The Status event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "StatusOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WatchOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WatchOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Watch options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WorkflowDispatchOptions",
    jsii_struct_bases=[],
    name_mapping={},
)
class WorkflowDispatchOptions:
    def __init__(self) -> None:
        '''The Workflow dispatch event accepts no options.'''
        self._values: typing.Dict[str, typing.Any] = {}

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowDispatchOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WorkflowRunOptions",
    jsii_struct_bases=[],
    name_mapping={"types": "types"},
)
class WorkflowRunOptions:
    def __init__(
        self,
        *,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Workflow run options.

        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowRunOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.WorkflowTriggers",
    jsii_struct_bases=[],
    name_mapping={
        "check_run": "checkRun",
        "check_suite": "checkSuite",
        "create": "create",
        "delete": "delete",
        "deployment": "deployment",
        "deployment_status": "deploymentStatus",
        "fork": "fork",
        "gollum": "gollum",
        "issue_comment": "issueComment",
        "issues": "issues",
        "label": "label",
        "milestone": "milestone",
        "page_build": "pageBuild",
        "project": "project",
        "project_card": "projectCard",
        "project_column": "projectColumn",
        "public": "public",
        "pull_request": "pullRequest",
        "pull_request_review": "pullRequestReview",
        "pull_request_review_comment": "pullRequestReviewComment",
        "pull_request_target": "pullRequestTarget",
        "push": "push",
        "registry_package": "registryPackage",
        "release": "release",
        "repository_dispatch": "repositoryDispatch",
        "schedule": "schedule",
        "status": "status",
        "watch": "watch",
        "workflow_dispatch": "workflowDispatch",
        "workflow_run": "workflowRun",
    },
)
class WorkflowTriggers:
    def __init__(
        self,
        *,
        check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[str, typing.Any]]] = None,
        check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[str, typing.Any]]] = None,
        create: typing.Optional[typing.Union[CreateOptions, typing.Dict[str, typing.Any]]] = None,
        delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[str, typing.Any]]] = None,
        deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[str, typing.Any]]] = None,
        deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[str, typing.Any]]] = None,
        fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[str, typing.Any]]] = None,
        gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[str, typing.Any]]] = None,
        issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[str, typing.Any]]] = None,
        issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[str, typing.Any]]] = None,
        label: typing.Optional[typing.Union[LabelOptions, typing.Dict[str, typing.Any]]] = None,
        milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[str, typing.Any]]] = None,
        page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[str, typing.Any]]] = None,
        project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[str, typing.Any]]] = None,
        project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[str, typing.Any]]] = None,
        project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[str, typing.Any]]] = None,
        public: typing.Optional[typing.Union[PublicOptions, typing.Dict[str, typing.Any]]] = None,
        pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[str, typing.Any]]] = None,
        pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[str, typing.Any]]] = None,
        pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[str, typing.Any]]] = None,
        pull_request_target: typing.Optional[typing.Union["PullRequestTargetOptions", typing.Dict[str, typing.Any]]] = None,
        push: typing.Optional[typing.Union[PushOptions, typing.Dict[str, typing.Any]]] = None,
        registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[str, typing.Any]]] = None,
        release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[str, typing.Any]]] = None,
        repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[str, typing.Any]]] = None,
        schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[str, typing.Any]]]] = None,
        status: typing.Optional[typing.Union[StatusOptions, typing.Dict[str, typing.Any]]] = None,
        watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[str, typing.Any]]] = None,
        workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[str, typing.Any]]] = None,
        workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[str, typing.Any]]] = None,
    ) -> None:
        '''The set of available triggers for GitHub Workflows.

        :param check_run: Runs your workflow anytime the check_run event occurs.
        :param check_suite: Runs your workflow anytime the check_suite event occurs.
        :param create: Runs your workflow anytime someone creates a branch or tag, which triggers the create event.
        :param delete: Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.
        :param deployment: Runs your workflow anytime someone creates a deployment, which triggers the deployment event. Deployments created with a commit SHA may not have a Git ref.
        :param deployment_status: Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event. Deployments created with a commit SHA may not have a Git ref.
        :param fork: Runs your workflow anytime when someone forks a repository, which triggers the fork event.
        :param gollum: Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.
        :param issue_comment: Runs your workflow anytime the issue_comment event occurs.
        :param issues: Runs your workflow anytime the issues event occurs.
        :param label: Runs your workflow anytime the label event occurs.
        :param milestone: Runs your workflow anytime the milestone event occurs.
        :param page_build: Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.
        :param project: Runs your workflow anytime the project event occurs.
        :param project_card: Runs your workflow anytime the project_card event occurs.
        :param project_column: Runs your workflow anytime the project_column event occurs.
        :param public: Runs your workflow anytime someone makes a private repository public, which triggers the public event.
        :param pull_request: Runs your workflow anytime the pull_request event occurs.
        :param pull_request_review: Runs your workflow anytime the pull_request_review event occurs.
        :param pull_request_review_comment: Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.
        :param pull_request_target: This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does. This prevents executing unsafe workflow code from the head of the pull request that could alter your repository or steal any secrets you use in your workflow. This event allows you to do things like create workflows that label and comment on pull requests based on the contents of the event payload. WARNING: The ``pull_request_target`` event is granted read/write repository token and can access secrets, even when it is triggered from a fork. Although the workflow runs in the context of the base of the pull request, you should make sure that you do not check out, build, or run untrusted code from the pull request with this event. Additionally, any caches share the same scope as the base branch, and to help prevent cache poisoning, you should not save the cache if there is a possibility that the cache contents were altered.
        :param push: Runs your workflow when someone pushes to a repository branch, which triggers the push event.
        :param registry_package: Runs your workflow anytime a package is published or updated.
        :param release: Runs your workflow anytime the release event occurs.
        :param repository_dispatch: You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.
        :param schedule: You can schedule a workflow to run at specific UTC times using POSIX cron syntax. Scheduled workflows run on the latest commit on the default or base branch. The shortest interval you can run scheduled workflows is once every 5 minutes.
        :param status: Runs your workflow anytime the status of a Git commit changes, which triggers the status event.
        :param watch: Runs your workflow anytime the watch event occurs.
        :param workflow_dispatch: You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow. When the workflow runs, you can access the input values in the github.event.inputs context.
        :param workflow_run: This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow. A workflow run is triggered regardless of the result of the previous workflow.

        :see: https://docs.github.com/en/actions/reference/events-that-trigger-workflows
        '''
        if isinstance(check_run, dict):
            check_run = CheckRunOptions(**check_run)
        if isinstance(check_suite, dict):
            check_suite = CheckSuiteOptions(**check_suite)
        if isinstance(create, dict):
            create = CreateOptions(**create)
        if isinstance(delete, dict):
            delete = DeleteOptions(**delete)
        if isinstance(deployment, dict):
            deployment = DeploymentOptions(**deployment)
        if isinstance(deployment_status, dict):
            deployment_status = DeploymentStatusOptions(**deployment_status)
        if isinstance(fork, dict):
            fork = ForkOptions(**fork)
        if isinstance(gollum, dict):
            gollum = GollumOptions(**gollum)
        if isinstance(issue_comment, dict):
            issue_comment = IssueCommentOptions(**issue_comment)
        if isinstance(issues, dict):
            issues = IssuesOptions(**issues)
        if isinstance(label, dict):
            label = LabelOptions(**label)
        if isinstance(milestone, dict):
            milestone = MilestoneOptions(**milestone)
        if isinstance(page_build, dict):
            page_build = PageBuildOptions(**page_build)
        if isinstance(project, dict):
            project = ProjectOptions(**project)
        if isinstance(project_card, dict):
            project_card = ProjectCardOptions(**project_card)
        if isinstance(project_column, dict):
            project_column = ProjectColumnOptions(**project_column)
        if isinstance(public, dict):
            public = PublicOptions(**public)
        if isinstance(pull_request, dict):
            pull_request = PullRequestOptions(**pull_request)
        if isinstance(pull_request_review, dict):
            pull_request_review = PullRequestReviewOptions(**pull_request_review)
        if isinstance(pull_request_review_comment, dict):
            pull_request_review_comment = PullRequestReviewCommentOptions(**pull_request_review_comment)
        if isinstance(pull_request_target, dict):
            pull_request_target = PullRequestTargetOptions(**pull_request_target)
        if isinstance(push, dict):
            push = PushOptions(**push)
        if isinstance(registry_package, dict):
            registry_package = RegistryPackageOptions(**registry_package)
        if isinstance(release, dict):
            release = ReleaseOptions(**release)
        if isinstance(repository_dispatch, dict):
            repository_dispatch = RepositoryDispatchOptions(**repository_dispatch)
        if isinstance(status, dict):
            status = StatusOptions(**status)
        if isinstance(watch, dict):
            watch = WatchOptions(**watch)
        if isinstance(workflow_dispatch, dict):
            workflow_dispatch = WorkflowDispatchOptions(**workflow_dispatch)
        if isinstance(workflow_run, dict):
            workflow_run = WorkflowRunOptions(**workflow_run)
        if __debug__:
            def stub(
                *,
                check_run: typing.Optional[typing.Union[CheckRunOptions, typing.Dict[str, typing.Any]]] = None,
                check_suite: typing.Optional[typing.Union[CheckSuiteOptions, typing.Dict[str, typing.Any]]] = None,
                create: typing.Optional[typing.Union[CreateOptions, typing.Dict[str, typing.Any]]] = None,
                delete: typing.Optional[typing.Union[DeleteOptions, typing.Dict[str, typing.Any]]] = None,
                deployment: typing.Optional[typing.Union[DeploymentOptions, typing.Dict[str, typing.Any]]] = None,
                deployment_status: typing.Optional[typing.Union[DeploymentStatusOptions, typing.Dict[str, typing.Any]]] = None,
                fork: typing.Optional[typing.Union[ForkOptions, typing.Dict[str, typing.Any]]] = None,
                gollum: typing.Optional[typing.Union[GollumOptions, typing.Dict[str, typing.Any]]] = None,
                issue_comment: typing.Optional[typing.Union[IssueCommentOptions, typing.Dict[str, typing.Any]]] = None,
                issues: typing.Optional[typing.Union[IssuesOptions, typing.Dict[str, typing.Any]]] = None,
                label: typing.Optional[typing.Union[LabelOptions, typing.Dict[str, typing.Any]]] = None,
                milestone: typing.Optional[typing.Union[MilestoneOptions, typing.Dict[str, typing.Any]]] = None,
                page_build: typing.Optional[typing.Union[PageBuildOptions, typing.Dict[str, typing.Any]]] = None,
                project: typing.Optional[typing.Union[ProjectOptions, typing.Dict[str, typing.Any]]] = None,
                project_card: typing.Optional[typing.Union[ProjectCardOptions, typing.Dict[str, typing.Any]]] = None,
                project_column: typing.Optional[typing.Union[ProjectColumnOptions, typing.Dict[str, typing.Any]]] = None,
                public: typing.Optional[typing.Union[PublicOptions, typing.Dict[str, typing.Any]]] = None,
                pull_request: typing.Optional[typing.Union[PullRequestOptions, typing.Dict[str, typing.Any]]] = None,
                pull_request_review: typing.Optional[typing.Union[PullRequestReviewOptions, typing.Dict[str, typing.Any]]] = None,
                pull_request_review_comment: typing.Optional[typing.Union[PullRequestReviewCommentOptions, typing.Dict[str, typing.Any]]] = None,
                pull_request_target: typing.Optional[typing.Union["PullRequestTargetOptions", typing.Dict[str, typing.Any]]] = None,
                push: typing.Optional[typing.Union[PushOptions, typing.Dict[str, typing.Any]]] = None,
                registry_package: typing.Optional[typing.Union[RegistryPackageOptions, typing.Dict[str, typing.Any]]] = None,
                release: typing.Optional[typing.Union[ReleaseOptions, typing.Dict[str, typing.Any]]] = None,
                repository_dispatch: typing.Optional[typing.Union[RepositoryDispatchOptions, typing.Dict[str, typing.Any]]] = None,
                schedule: typing.Optional[typing.Sequence[typing.Union[CronScheduleOptions, typing.Dict[str, typing.Any]]]] = None,
                status: typing.Optional[typing.Union[StatusOptions, typing.Dict[str, typing.Any]]] = None,
                watch: typing.Optional[typing.Union[WatchOptions, typing.Dict[str, typing.Any]]] = None,
                workflow_dispatch: typing.Optional[typing.Union[WorkflowDispatchOptions, typing.Dict[str, typing.Any]]] = None,
                workflow_run: typing.Optional[typing.Union[WorkflowRunOptions, typing.Dict[str, typing.Any]]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument check_run", value=check_run, expected_type=type_hints["check_run"])
            check_type(argname="argument check_suite", value=check_suite, expected_type=type_hints["check_suite"])
            check_type(argname="argument create", value=create, expected_type=type_hints["create"])
            check_type(argname="argument delete", value=delete, expected_type=type_hints["delete"])
            check_type(argname="argument deployment", value=deployment, expected_type=type_hints["deployment"])
            check_type(argname="argument deployment_status", value=deployment_status, expected_type=type_hints["deployment_status"])
            check_type(argname="argument fork", value=fork, expected_type=type_hints["fork"])
            check_type(argname="argument gollum", value=gollum, expected_type=type_hints["gollum"])
            check_type(argname="argument issue_comment", value=issue_comment, expected_type=type_hints["issue_comment"])
            check_type(argname="argument issues", value=issues, expected_type=type_hints["issues"])
            check_type(argname="argument label", value=label, expected_type=type_hints["label"])
            check_type(argname="argument milestone", value=milestone, expected_type=type_hints["milestone"])
            check_type(argname="argument page_build", value=page_build, expected_type=type_hints["page_build"])
            check_type(argname="argument project", value=project, expected_type=type_hints["project"])
            check_type(argname="argument project_card", value=project_card, expected_type=type_hints["project_card"])
            check_type(argname="argument project_column", value=project_column, expected_type=type_hints["project_column"])
            check_type(argname="argument public", value=public, expected_type=type_hints["public"])
            check_type(argname="argument pull_request", value=pull_request, expected_type=type_hints["pull_request"])
            check_type(argname="argument pull_request_review", value=pull_request_review, expected_type=type_hints["pull_request_review"])
            check_type(argname="argument pull_request_review_comment", value=pull_request_review_comment, expected_type=type_hints["pull_request_review_comment"])
            check_type(argname="argument pull_request_target", value=pull_request_target, expected_type=type_hints["pull_request_target"])
            check_type(argname="argument push", value=push, expected_type=type_hints["push"])
            check_type(argname="argument registry_package", value=registry_package, expected_type=type_hints["registry_package"])
            check_type(argname="argument release", value=release, expected_type=type_hints["release"])
            check_type(argname="argument repository_dispatch", value=repository_dispatch, expected_type=type_hints["repository_dispatch"])
            check_type(argname="argument schedule", value=schedule, expected_type=type_hints["schedule"])
            check_type(argname="argument status", value=status, expected_type=type_hints["status"])
            check_type(argname="argument watch", value=watch, expected_type=type_hints["watch"])
            check_type(argname="argument workflow_dispatch", value=workflow_dispatch, expected_type=type_hints["workflow_dispatch"])
            check_type(argname="argument workflow_run", value=workflow_run, expected_type=type_hints["workflow_run"])
        self._values: typing.Dict[str, typing.Any] = {}
        if check_run is not None:
            self._values["check_run"] = check_run
        if check_suite is not None:
            self._values["check_suite"] = check_suite
        if create is not None:
            self._values["create"] = create
        if delete is not None:
            self._values["delete"] = delete
        if deployment is not None:
            self._values["deployment"] = deployment
        if deployment_status is not None:
            self._values["deployment_status"] = deployment_status
        if fork is not None:
            self._values["fork"] = fork
        if gollum is not None:
            self._values["gollum"] = gollum
        if issue_comment is not None:
            self._values["issue_comment"] = issue_comment
        if issues is not None:
            self._values["issues"] = issues
        if label is not None:
            self._values["label"] = label
        if milestone is not None:
            self._values["milestone"] = milestone
        if page_build is not None:
            self._values["page_build"] = page_build
        if project is not None:
            self._values["project"] = project
        if project_card is not None:
            self._values["project_card"] = project_card
        if project_column is not None:
            self._values["project_column"] = project_column
        if public is not None:
            self._values["public"] = public
        if pull_request is not None:
            self._values["pull_request"] = pull_request
        if pull_request_review is not None:
            self._values["pull_request_review"] = pull_request_review
        if pull_request_review_comment is not None:
            self._values["pull_request_review_comment"] = pull_request_review_comment
        if pull_request_target is not None:
            self._values["pull_request_target"] = pull_request_target
        if push is not None:
            self._values["push"] = push
        if registry_package is not None:
            self._values["registry_package"] = registry_package
        if release is not None:
            self._values["release"] = release
        if repository_dispatch is not None:
            self._values["repository_dispatch"] = repository_dispatch
        if schedule is not None:
            self._values["schedule"] = schedule
        if status is not None:
            self._values["status"] = status
        if watch is not None:
            self._values["watch"] = watch
        if workflow_dispatch is not None:
            self._values["workflow_dispatch"] = workflow_dispatch
        if workflow_run is not None:
            self._values["workflow_run"] = workflow_run

    @builtins.property
    def check_run(self) -> typing.Optional[CheckRunOptions]:
        '''Runs your workflow anytime the check_run event occurs.'''
        result = self._values.get("check_run")
        return typing.cast(typing.Optional[CheckRunOptions], result)

    @builtins.property
    def check_suite(self) -> typing.Optional[CheckSuiteOptions]:
        '''Runs your workflow anytime the check_suite event occurs.'''
        result = self._values.get("check_suite")
        return typing.cast(typing.Optional[CheckSuiteOptions], result)

    @builtins.property
    def create(self) -> typing.Optional[CreateOptions]:
        '''Runs your workflow anytime someone creates a branch or tag, which triggers the create event.'''
        result = self._values.get("create")
        return typing.cast(typing.Optional[CreateOptions], result)

    @builtins.property
    def delete(self) -> typing.Optional[DeleteOptions]:
        '''Runs your workflow anytime someone deletes a branch or tag, which triggers the delete event.'''
        result = self._values.get("delete")
        return typing.cast(typing.Optional[DeleteOptions], result)

    @builtins.property
    def deployment(self) -> typing.Optional[DeploymentOptions]:
        '''Runs your workflow anytime someone creates a deployment, which triggers the deployment event.

        Deployments created with a commit SHA may not have
        a Git ref.
        '''
        result = self._values.get("deployment")
        return typing.cast(typing.Optional[DeploymentOptions], result)

    @builtins.property
    def deployment_status(self) -> typing.Optional[DeploymentStatusOptions]:
        '''Runs your workflow anytime a third party provides a deployment status, which triggers the deployment_status event.

        Deployments created with a
        commit SHA may not have a Git ref.
        '''
        result = self._values.get("deployment_status")
        return typing.cast(typing.Optional[DeploymentStatusOptions], result)

    @builtins.property
    def fork(self) -> typing.Optional[ForkOptions]:
        '''Runs your workflow anytime when someone forks a repository, which triggers the fork event.'''
        result = self._values.get("fork")
        return typing.cast(typing.Optional[ForkOptions], result)

    @builtins.property
    def gollum(self) -> typing.Optional[GollumOptions]:
        '''Runs your workflow when someone creates or updates a Wiki page, which triggers the gollum event.'''
        result = self._values.get("gollum")
        return typing.cast(typing.Optional[GollumOptions], result)

    @builtins.property
    def issue_comment(self) -> typing.Optional[IssueCommentOptions]:
        '''Runs your workflow anytime the issue_comment event occurs.'''
        result = self._values.get("issue_comment")
        return typing.cast(typing.Optional[IssueCommentOptions], result)

    @builtins.property
    def issues(self) -> typing.Optional[IssuesOptions]:
        '''Runs your workflow anytime the issues event occurs.'''
        result = self._values.get("issues")
        return typing.cast(typing.Optional[IssuesOptions], result)

    @builtins.property
    def label(self) -> typing.Optional[LabelOptions]:
        '''Runs your workflow anytime the label event occurs.'''
        result = self._values.get("label")
        return typing.cast(typing.Optional[LabelOptions], result)

    @builtins.property
    def milestone(self) -> typing.Optional[MilestoneOptions]:
        '''Runs your workflow anytime the milestone event occurs.'''
        result = self._values.get("milestone")
        return typing.cast(typing.Optional[MilestoneOptions], result)

    @builtins.property
    def page_build(self) -> typing.Optional[PageBuildOptions]:
        '''Runs your workflow anytime someone pushes to a GitHub Pages-enabled branch, which triggers the page_build event.'''
        result = self._values.get("page_build")
        return typing.cast(typing.Optional[PageBuildOptions], result)

    @builtins.property
    def project(self) -> typing.Optional[ProjectOptions]:
        '''Runs your workflow anytime the project event occurs.'''
        result = self._values.get("project")
        return typing.cast(typing.Optional[ProjectOptions], result)

    @builtins.property
    def project_card(self) -> typing.Optional[ProjectCardOptions]:
        '''Runs your workflow anytime the project_card event occurs.'''
        result = self._values.get("project_card")
        return typing.cast(typing.Optional[ProjectCardOptions], result)

    @builtins.property
    def project_column(self) -> typing.Optional[ProjectColumnOptions]:
        '''Runs your workflow anytime the project_column event occurs.'''
        result = self._values.get("project_column")
        return typing.cast(typing.Optional[ProjectColumnOptions], result)

    @builtins.property
    def public(self) -> typing.Optional[PublicOptions]:
        '''Runs your workflow anytime someone makes a private repository public, which triggers the public event.'''
        result = self._values.get("public")
        return typing.cast(typing.Optional[PublicOptions], result)

    @builtins.property
    def pull_request(self) -> typing.Optional[PullRequestOptions]:
        '''Runs your workflow anytime the pull_request event occurs.'''
        result = self._values.get("pull_request")
        return typing.cast(typing.Optional[PullRequestOptions], result)

    @builtins.property
    def pull_request_review(self) -> typing.Optional[PullRequestReviewOptions]:
        '''Runs your workflow anytime the pull_request_review event occurs.'''
        result = self._values.get("pull_request_review")
        return typing.cast(typing.Optional[PullRequestReviewOptions], result)

    @builtins.property
    def pull_request_review_comment(
        self,
    ) -> typing.Optional[PullRequestReviewCommentOptions]:
        '''Runs your workflow anytime a comment on a pull request's unified diff is modified, which triggers the pull_request_review_comment event.'''
        result = self._values.get("pull_request_review_comment")
        return typing.cast(typing.Optional[PullRequestReviewCommentOptions], result)

    @builtins.property
    def pull_request_target(self) -> typing.Optional["PullRequestTargetOptions"]:
        '''This event runs in the context of the base of the pull request, rather than in the merge commit as the pull_request event does.

        This prevents
        executing unsafe workflow code from the head of the pull request that
        could alter your repository or steal any secrets you use in your workflow.
        This event allows you to do things like create workflows that label and
        comment on pull requests based on the contents of the event payload.

        WARNING: The ``pull_request_target`` event is granted read/write repository
        token and can access secrets, even when it is triggered from a fork.
        Although the workflow runs in the context of the base of the pull request,
        you should make sure that you do not check out, build, or run untrusted
        code from the pull request with this event. Additionally, any caches
        share the same scope as the base branch, and to help prevent cache
        poisoning, you should not save the cache if there is a possibility that
        the cache contents were altered.

        :see: https://securitylab.github.com/research/github-actions-preventing-pwn-requests
        '''
        result = self._values.get("pull_request_target")
        return typing.cast(typing.Optional["PullRequestTargetOptions"], result)

    @builtins.property
    def push(self) -> typing.Optional[PushOptions]:
        '''Runs your workflow when someone pushes to a repository branch, which triggers the push event.'''
        result = self._values.get("push")
        return typing.cast(typing.Optional[PushOptions], result)

    @builtins.property
    def registry_package(self) -> typing.Optional[RegistryPackageOptions]:
        '''Runs your workflow anytime a package is published or updated.'''
        result = self._values.get("registry_package")
        return typing.cast(typing.Optional[RegistryPackageOptions], result)

    @builtins.property
    def release(self) -> typing.Optional[ReleaseOptions]:
        '''Runs your workflow anytime the release event occurs.'''
        result = self._values.get("release")
        return typing.cast(typing.Optional[ReleaseOptions], result)

    @builtins.property
    def repository_dispatch(self) -> typing.Optional[RepositoryDispatchOptions]:
        '''You can use the GitHub API to trigger a webhook event called repository_dispatch when you want to trigger a workflow for activity that happens outside of GitHub.'''
        result = self._values.get("repository_dispatch")
        return typing.cast(typing.Optional[RepositoryDispatchOptions], result)

    @builtins.property
    def schedule(self) -> typing.Optional[typing.List[CronScheduleOptions]]:
        '''You can schedule a workflow to run at specific UTC times using POSIX cron syntax.

        Scheduled workflows run on the latest commit on the default or
        base branch. The shortest interval you can run scheduled workflows is
        once every 5 minutes.

        :see: https://pubs.opengroup.org/onlinepubs/9699919799/utilities/crontab.html#tag_20_25_07
        '''
        result = self._values.get("schedule")
        return typing.cast(typing.Optional[typing.List[CronScheduleOptions]], result)

    @builtins.property
    def status(self) -> typing.Optional[StatusOptions]:
        '''Runs your workflow anytime the status of a Git commit changes, which triggers the status event.'''
        result = self._values.get("status")
        return typing.cast(typing.Optional[StatusOptions], result)

    @builtins.property
    def watch(self) -> typing.Optional[WatchOptions]:
        '''Runs your workflow anytime the watch event occurs.'''
        result = self._values.get("watch")
        return typing.cast(typing.Optional[WatchOptions], result)

    @builtins.property
    def workflow_dispatch(self) -> typing.Optional[WorkflowDispatchOptions]:
        '''You can configure custom-defined input properties, default input values, and required inputs for the event directly in your workflow.

        When the
        workflow runs, you can access the input values in the github.event.inputs
        context.
        '''
        result = self._values.get("workflow_dispatch")
        return typing.cast(typing.Optional[WorkflowDispatchOptions], result)

    @builtins.property
    def workflow_run(self) -> typing.Optional[WorkflowRunOptions]:
        '''This event occurs when a workflow run is requested or completed, and allows you to execute a workflow based on the finished result of another workflow.

        A workflow run is triggered regardless of the result of the
        previous workflow.
        '''
        result = self._values.get("workflow_run")
        return typing.cast(typing.Optional[WorkflowRunOptions], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "WorkflowTriggers(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


class YamlFile(metaclass=jsii.JSIIMeta, jsii_type="cdk-pipelines-github.YamlFile"):
    '''Represents a Yaml File.'''

    def __init__(self, file_path: builtins.str, *, obj: typing.Any = None) -> None:
        '''
        :param file_path: -
        :param obj: The object that will be serialized. You can modify the object's contents before synthesis. Default: {} an empty object
        '''
        if __debug__:
            def stub(file_path: builtins.str, *, obj: typing.Any = None) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument file_path", value=file_path, expected_type=type_hints["file_path"])
        options = YamlFileOptions(obj=obj)

        jsii.create(self.__class__, self, [file_path, options])

    @jsii.member(jsii_name="patch")
    def patch(self, *patches: JsonPatch) -> None:
        '''Applies an RFC 6902 JSON-patch to the synthesized object file. See https://datatracker.ietf.org/doc/html/rfc6902 for more information.

        For example, with the following yaml file Example::

           name: deploy
           on:
              push:
                branches:
                  - main
              workflow_dispatch: {}
           ...

        modified in the following way::

           pipeline.workflowFile.patch(JsonPatch.add("/on/workflow_call", "{}"));
           pipeline.workflowFile.patch(JsonPatch.remove("/on/workflow_dispatch"));

        would result in the following yaml file::

           name: deploy
           on:
              push:
                branches:
                  - main
              workflow_call: {}
           ...

        :param patches: - The patch operations to apply.
        '''
        if __debug__:
            def stub(*patches: JsonPatch) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument patches", value=patches, expected_type=typing.Tuple[type_hints["patches"], ...]) # pyright: ignore [reportGeneralTypeIssues]
        return typing.cast(None, jsii.invoke(self, "patch", [*patches]))

    @jsii.member(jsii_name="toYaml")
    def to_yaml(self) -> builtins.str:
        '''Returns the patched yaml file.'''
        return typing.cast(builtins.str, jsii.invoke(self, "toYaml", []))

    @jsii.member(jsii_name="update")
    def update(self, obj: typing.Any) -> None:
        '''Update the output object.

        :param obj: -
        '''
        if __debug__:
            def stub(obj: typing.Any) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        return typing.cast(None, jsii.invoke(self, "update", [obj]))

    @jsii.member(jsii_name="writeFile")
    def write_file(self) -> None:
        '''Write the patched yaml file to the specified location.'''
        return typing.cast(None, jsii.invoke(self, "writeFile", []))

    @builtins.property
    @jsii.member(jsii_name="commentAtTop")
    def comment_at_top(self) -> typing.Optional[builtins.str]:
        '''A comment to be added to the top of the YAML file.

        Can be multiline. All non-empty line are pefixed with '# '. Empty lines are kept, but not commented.

        For example::

           pipeline.workflowFile.commentAtTop =
           `AUTOGENERATED FILE, DO NOT EDIT!
           See ReadMe.md
           `;

        Results in YAML::

           # AUTOGENERATED FILE, DO NOT EDIT!
           # See ReadMe.md

           name: deploy
           ...
        '''
        return typing.cast(typing.Optional[builtins.str], jsii.get(self, "commentAtTop"))

    @comment_at_top.setter
    def comment_at_top(self, value: typing.Optional[builtins.str]) -> None:
        if __debug__:
            def stub(value: typing.Optional[builtins.str]) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument value", value=value, expected_type=type_hints["value"])
        jsii.set(self, "commentAtTop", value)


@jsii.data_type(
    jsii_type="cdk-pipelines-github.YamlFileOptions",
    jsii_struct_bases=[],
    name_mapping={"obj": "obj"},
)
class YamlFileOptions:
    def __init__(self, *, obj: typing.Any = None) -> None:
        '''Options for ``YamlFile``.

        :param obj: The object that will be serialized. You can modify the object's contents before synthesis. Default: {} an empty object
        '''
        if __debug__:
            def stub(*, obj: typing.Any = None) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument obj", value=obj, expected_type=type_hints["obj"])
        self._values: typing.Dict[str, typing.Any] = {}
        if obj is not None:
            self._values["obj"] = obj

    @builtins.property
    def obj(self) -> typing.Any:
        '''The object that will be serialized.

        You can modify the object's contents
        before synthesis.

        :default: {} an empty object
        '''
        result = self._values.get("obj")
        return typing.cast(typing.Any, result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "YamlFileOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


@jsii.data_type(
    jsii_type="cdk-pipelines-github.PullRequestTargetOptions",
    jsii_struct_bases=[PushOptions],
    name_mapping={
        "branches": "branches",
        "paths": "paths",
        "tags": "tags",
        "types": "types",
    },
)
class PullRequestTargetOptions(PushOptions):
    def __init__(
        self,
        *,
        branches: typing.Optional[typing.Sequence[builtins.str]] = None,
        paths: typing.Optional[typing.Sequence[builtins.str]] = None,
        tags: typing.Optional[typing.Sequence[builtins.str]] = None,
        types: typing.Optional[typing.Sequence[builtins.str]] = None,
    ) -> None:
        '''Pull request target options.

        :param branches: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param paths: When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths. Path filters are not evaluated for pushes to tags.
        :param tags: When using the push and pull_request events, you can configure a workflow to run on specific branches or tags. For a pull_request event, only branches and tags on the base are evaluated. If you define only tags or only branches, the workflow won't run for events affecting the undefined Git ref.
        :param types: Which activity types to trigger on.
        '''
        if __debug__:
            def stub(
                *,
                branches: typing.Optional[typing.Sequence[builtins.str]] = None,
                paths: typing.Optional[typing.Sequence[builtins.str]] = None,
                tags: typing.Optional[typing.Sequence[builtins.str]] = None,
                types: typing.Optional[typing.Sequence[builtins.str]] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument branches", value=branches, expected_type=type_hints["branches"])
            check_type(argname="argument paths", value=paths, expected_type=type_hints["paths"])
            check_type(argname="argument tags", value=tags, expected_type=type_hints["tags"])
            check_type(argname="argument types", value=types, expected_type=type_hints["types"])
        self._values: typing.Dict[str, typing.Any] = {}
        if branches is not None:
            self._values["branches"] = branches
        if paths is not None:
            self._values["paths"] = paths
        if tags is not None:
            self._values["tags"] = tags
        if types is not None:
            self._values["types"] = types

    @builtins.property
    def branches(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("branches")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def paths(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run when at least one file does not match paths-ignore or at least one modified file matches the configured paths.

        Path filters are not
        evaluated for pushes to tags.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("paths")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def tags(self) -> typing.Optional[typing.List[builtins.str]]:
        '''When using the push and pull_request events, you can configure a workflow to run on specific branches or tags.

        For a pull_request event, only
        branches and tags on the base are evaluated. If you define only tags or
        only branches, the workflow won't run for events affecting the undefined
        Git ref.

        :see: https://docs.github.com/en/actions/reference/workflow-syntax-for-github-actions#filter-pattern-cheat-sheet
        '''
        result = self._values.get("tags")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    @builtins.property
    def types(self) -> typing.Optional[typing.List[builtins.str]]:
        '''Which activity types to trigger on.

        :defaults: - all activity types
        '''
        result = self._values.get("types")
        return typing.cast(typing.Optional[typing.List[builtins.str]], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "PullRequestTargetOptions(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "AddGitHubStageOptions",
    "AwsCredentials",
    "AwsCredentialsProvider",
    "AwsCredentialsSecrets",
    "CheckRunOptions",
    "CheckSuiteOptions",
    "ContainerCredentials",
    "ContainerOptions",
    "CreateOptions",
    "CronScheduleOptions",
    "DeleteOptions",
    "DeploymentOptions",
    "DeploymentStatusOptions",
    "DockerCredential",
    "DockerHubCredentialSecrets",
    "ExternalDockerCredentialSecrets",
    "ForkOptions",
    "GitHubActionRole",
    "GitHubActionRoleProps",
    "GitHubActionStep",
    "GitHubActionStepProps",
    "GitHubSecretsProviderProps",
    "GitHubWorkflow",
    "GitHubWorkflowProps",
    "GollumOptions",
    "IssueCommentOptions",
    "IssuesOptions",
    "Job",
    "JobDefaults",
    "JobMatrix",
    "JobPermission",
    "JobPermissions",
    "JobSettings",
    "JobStep",
    "JobStepOutput",
    "JobStrategy",
    "JsonPatch",
    "LabelOptions",
    "MilestoneOptions",
    "OpenIdConnectProviderProps",
    "PageBuildOptions",
    "ProjectCardOptions",
    "ProjectColumnOptions",
    "ProjectOptions",
    "PublicOptions",
    "PullRequestOptions",
    "PullRequestReviewCommentOptions",
    "PullRequestReviewOptions",
    "PullRequestTargetOptions",
    "PushOptions",
    "RegistryPackageOptions",
    "ReleaseOptions",
    "RepositoryDispatchOptions",
    "RunSettings",
    "Runner",
    "StackCapabilities",
    "StatusOptions",
    "WatchOptions",
    "WorkflowDispatchOptions",
    "WorkflowRunOptions",
    "WorkflowTriggers",
    "YamlFile",
    "YamlFileOptions",
]

publication.publish()
