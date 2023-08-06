'''
# CDK Backup Plan

![Build](https://github.com/aws-samples/cdk-backup-plan/workflows/build/badge.svg)
![Release](https://github.com/aws-samples/cdk-backup-plan/workflows/release/badge.svg)

Provides an easy to use reusable CDK construct to create [Backup Plans](https://docs.aws.amazon.com/aws-backup/latest/devguide/about-backup-plans.html) using [AWS Backups](https://docs.aws.amazon.com/aws-backup/latest/devguide/whatisbackup.html). It allows to indicate how frequently and what resources to backup.

> **NOTE:** More details on all the available arguments can be found [here](API.md)

## Install

NPM install:

```sh
npm install cdk-backup-plan
```

PyPi install:

```sh
pip install cdk-backup-plan
```

## Usage

```python
// ...
import { Backup } from "cdk-backup-plan";

// ...
const vpc = new ec2.Vpc(stack, "TestVPC");
const engine = rds.DatabaseInstanceEngine.postgres({
  version: rds.PostgresEngineVersion.VER_12_3,
});
// create rds DB
const db = new rds.DatabaseInstance(stack, "TestInstance", {
  engine,
  vpc,
  credentials: rds.Credentials.fromGeneratedSecret("postgres"),
});
// create a backup plan for `db`
new Backup(stack, "TestBk", {
  backupPlanName: "TestPkPlan",
  backupRateHour: 3, // backup every 3 hours
  backupCompletionWindow: cdk.Duration.hours(2), // backup should take up to 2 hours
  resources: [bk.BackupResource.fromRdsDatabaseInstance(db)],
});
// ...
```

Python usage:

```python
# ...
from cdk_backup_plan import Backup

# ...
vpc = ec2.Vpc(self, "TestVPC")
engine = rds.DatabaseInstanceEngine.postgres(
    version=rds.PostgresEngineVersion.VER_12_3,
)
db = rds.DatabaseInstance(self, "TestInstance",
    engine=engine,
    vpc=vpc,
    credentials=rds.Credentials.from_generated_secret("postgres"),
)
Backup(self, "TestBk",
    backup_plan_name="TestPkPlan",
    backup_rate_hour=3,
    backup_completion_window=Duration.hours(2),
    resources=[bk.BackupResource.from_rds_database_instance(db)],
)
# ...
```

> **NOTE:** [Tagging](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_backup.BackupResource.html#static-fromwbrtagkey-value-operation) and/or [ARN](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_backup.BackupResource.html#static-fromwbrarnarn) can be used to reference resources not directly available in the [static methods section](https://docs.aws.amazon.com/cdk/api/v2/docs/aws-cdk-lib.aws_backup.BackupResource.html#methods).
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
import aws_cdk.aws_backup
import constructs


class Backup(
    constructs.Construct,
    metaclass=jsii.JSIIMeta,
    jsii_type="cdk-backup-plan.Backup",
):
    '''Construct to create a Backup Plan with specific backing cadence.'''

    def __init__(
        self,
        scope: constructs.Construct,
        id: builtins.str,
        *,
        backup_plan_name: builtins.str,
        resources: typing.Sequence[aws_cdk.aws_backup.BackupResource],
        backup_completion_window: typing.Optional[aws_cdk.Duration] = None,
        backup_rate_hour: typing.Optional[jsii.Number] = None,
        backup_start_window: typing.Optional[aws_cdk.Duration] = None,
        delete_backup_after: typing.Optional[aws_cdk.Duration] = None,
        move_backup_to_cold_storage_after: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param scope: Construct's scope.
        :param id: Construct's id.
        :param backup_plan_name: The display name of the backup plan.
        :param resources: Resources to apply backup plan.
        :param backup_completion_window: The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup. Note: ``backupCompletionWindow`` must be at least 60 minutes greater than @backupStartWindows Default: - 3 hours
        :param backup_rate_hour: How frequently backup jobs would be started. Default: - 24 hours
        :param backup_start_window: The duration after a backup is scheduled before a job is canceled if it doesn't start successfully. Default: - 1 hour less than
        :param delete_backup_after: Specifies the duration after creation that a recovery point is deleted. Must be greater than moveToColdStorageAfter. Default: - 30 days
        :param move_backup_to_cold_storage_after: Specifies the duration after creation that a recovery point is moved to cold storage. Default: - recovery point is never moved to cold storage
        '''
        if __debug__:
            def stub(
                scope: constructs.Construct,
                id: builtins.str,
                *,
                backup_plan_name: builtins.str,
                resources: typing.Sequence[aws_cdk.aws_backup.BackupResource],
                backup_completion_window: typing.Optional[aws_cdk.Duration] = None,
                backup_rate_hour: typing.Optional[jsii.Number] = None,
                backup_start_window: typing.Optional[aws_cdk.Duration] = None,
                delete_backup_after: typing.Optional[aws_cdk.Duration] = None,
                move_backup_to_cold_storage_after: typing.Optional[aws_cdk.Duration] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument scope", value=scope, expected_type=type_hints["scope"])
            check_type(argname="argument id", value=id, expected_type=type_hints["id"])
        props = BackupProps(
            backup_plan_name=backup_plan_name,
            resources=resources,
            backup_completion_window=backup_completion_window,
            backup_rate_hour=backup_rate_hour,
            backup_start_window=backup_start_window,
            delete_backup_after=delete_backup_after,
            move_backup_to_cold_storage_after=move_backup_to_cold_storage_after,
        )

        jsii.create(self.__class__, self, [scope, id, props])

    @builtins.property
    @jsii.member(jsii_name="backupPlan")
    def backup_plan(self) -> aws_cdk.aws_backup.BackupPlan:
        '''Backup plan.'''
        return typing.cast(aws_cdk.aws_backup.BackupPlan, jsii.get(self, "backupPlan"))


@jsii.data_type(
    jsii_type="cdk-backup-plan.BackupProps",
    jsii_struct_bases=[],
    name_mapping={
        "backup_plan_name": "backupPlanName",
        "resources": "resources",
        "backup_completion_window": "backupCompletionWindow",
        "backup_rate_hour": "backupRateHour",
        "backup_start_window": "backupStartWindow",
        "delete_backup_after": "deleteBackupAfter",
        "move_backup_to_cold_storage_after": "moveBackupToColdStorageAfter",
    },
)
class BackupProps:
    def __init__(
        self,
        *,
        backup_plan_name: builtins.str,
        resources: typing.Sequence[aws_cdk.aws_backup.BackupResource],
        backup_completion_window: typing.Optional[aws_cdk.Duration] = None,
        backup_rate_hour: typing.Optional[jsii.Number] = None,
        backup_start_window: typing.Optional[aws_cdk.Duration] = None,
        delete_backup_after: typing.Optional[aws_cdk.Duration] = None,
        move_backup_to_cold_storage_after: typing.Optional[aws_cdk.Duration] = None,
    ) -> None:
        '''
        :param backup_plan_name: The display name of the backup plan.
        :param resources: Resources to apply backup plan.
        :param backup_completion_window: The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup. Note: ``backupCompletionWindow`` must be at least 60 minutes greater than @backupStartWindows Default: - 3 hours
        :param backup_rate_hour: How frequently backup jobs would be started. Default: - 24 hours
        :param backup_start_window: The duration after a backup is scheduled before a job is canceled if it doesn't start successfully. Default: - 1 hour less than
        :param delete_backup_after: Specifies the duration after creation that a recovery point is deleted. Must be greater than moveToColdStorageAfter. Default: - 30 days
        :param move_backup_to_cold_storage_after: Specifies the duration after creation that a recovery point is moved to cold storage. Default: - recovery point is never moved to cold storage
        '''
        if __debug__:
            def stub(
                *,
                backup_plan_name: builtins.str,
                resources: typing.Sequence[aws_cdk.aws_backup.BackupResource],
                backup_completion_window: typing.Optional[aws_cdk.Duration] = None,
                backup_rate_hour: typing.Optional[jsii.Number] = None,
                backup_start_window: typing.Optional[aws_cdk.Duration] = None,
                delete_backup_after: typing.Optional[aws_cdk.Duration] = None,
                move_backup_to_cold_storage_after: typing.Optional[aws_cdk.Duration] = None,
            ) -> None:
                ...
            type_hints = typing.get_type_hints(stub)
            check_type(argname="argument backup_plan_name", value=backup_plan_name, expected_type=type_hints["backup_plan_name"])
            check_type(argname="argument resources", value=resources, expected_type=type_hints["resources"])
            check_type(argname="argument backup_completion_window", value=backup_completion_window, expected_type=type_hints["backup_completion_window"])
            check_type(argname="argument backup_rate_hour", value=backup_rate_hour, expected_type=type_hints["backup_rate_hour"])
            check_type(argname="argument backup_start_window", value=backup_start_window, expected_type=type_hints["backup_start_window"])
            check_type(argname="argument delete_backup_after", value=delete_backup_after, expected_type=type_hints["delete_backup_after"])
            check_type(argname="argument move_backup_to_cold_storage_after", value=move_backup_to_cold_storage_after, expected_type=type_hints["move_backup_to_cold_storage_after"])
        self._values: typing.Dict[str, typing.Any] = {
            "backup_plan_name": backup_plan_name,
            "resources": resources,
        }
        if backup_completion_window is not None:
            self._values["backup_completion_window"] = backup_completion_window
        if backup_rate_hour is not None:
            self._values["backup_rate_hour"] = backup_rate_hour
        if backup_start_window is not None:
            self._values["backup_start_window"] = backup_start_window
        if delete_backup_after is not None:
            self._values["delete_backup_after"] = delete_backup_after
        if move_backup_to_cold_storage_after is not None:
            self._values["move_backup_to_cold_storage_after"] = move_backup_to_cold_storage_after

    @builtins.property
    def backup_plan_name(self) -> builtins.str:
        '''The display name of the backup plan.'''
        result = self._values.get("backup_plan_name")
        assert result is not None, "Required property 'backup_plan_name' is missing"
        return typing.cast(builtins.str, result)

    @builtins.property
    def resources(self) -> typing.List[aws_cdk.aws_backup.BackupResource]:
        '''Resources to apply backup plan.'''
        result = self._values.get("resources")
        assert result is not None, "Required property 'resources' is missing"
        return typing.cast(typing.List[aws_cdk.aws_backup.BackupResource], result)

    @builtins.property
    def backup_completion_window(self) -> typing.Optional[aws_cdk.Duration]:
        '''The duration after a backup job is successfully started before it must be completed or it is canceled by AWS Backup.

        Note: ``backupCompletionWindow`` must be at least 60 minutes greater
        than @backupStartWindows

        :default: - 3 hours
        '''
        result = self._values.get("backup_completion_window")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def backup_rate_hour(self) -> typing.Optional[jsii.Number]:
        '''How frequently backup jobs would be started.

        :default: - 24 hours
        '''
        result = self._values.get("backup_rate_hour")
        return typing.cast(typing.Optional[jsii.Number], result)

    @builtins.property
    def backup_start_window(self) -> typing.Optional[aws_cdk.Duration]:
        '''The duration after a backup is scheduled before a job is canceled if it doesn't start successfully.

        :default: - 1 hour less than

        :backupCompletionWindow: true
        '''
        result = self._values.get("backup_start_window")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def delete_backup_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''Specifies the duration after creation that a recovery point is deleted.

        Must be greater than moveToColdStorageAfter.

        :default: - 30 days
        '''
        result = self._values.get("delete_backup_after")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    @builtins.property
    def move_backup_to_cold_storage_after(self) -> typing.Optional[aws_cdk.Duration]:
        '''Specifies the duration after creation that a recovery point is moved to cold storage.

        :default: - recovery point is never moved to cold storage
        '''
        result = self._values.get("move_backup_to_cold_storage_after")
        return typing.cast(typing.Optional[aws_cdk.Duration], result)

    def __eq__(self, rhs: typing.Any) -> builtins.bool:
        return isinstance(rhs, self.__class__) and rhs._values == self._values

    def __ne__(self, rhs: typing.Any) -> builtins.bool:
        return not (rhs == self)

    def __repr__(self) -> str:
        return "BackupProps(%s)" % ", ".join(
            k + "=" + repr(v) for k, v in self._values.items()
        )


__all__ = [
    "Backup",
    "BackupProps",
]

publication.publish()
