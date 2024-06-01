import * as cdk from 'aws-cdk-lib';
import { Vpc } from 'aws-cdk-lib/aws-ec2';
import { Code, Function, Runtime } from 'aws-cdk-lib/aws-lambda';
import { Secret } from 'aws-cdk-lib/aws-secretsmanager';
import { Construct } from 'constructs';
import { LiveInfoScraperProps } from './props';

export class LiveInfoScraperStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props: LiveInfoScraperProps) {
    super(scope, id, props);

    // VPCの作成
    const vpc = new Vpc(this, 'AuroraVPC', {
      maxAzs: 2 // 可用性ゾーンの数
    });

    // データベースの認証情報をSecrets Managerで管理
    const secret = new Secret(this, 'DBSecret', {
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'admin' }),
        generateStringKey: 'password',
        excludeCharacters: '"@/\\',
      },
    });

    // Lambda関数の作成
    const lambdaFunction = new Function(this, 'AuroraLambdaFunction', {
      runtime: Runtime.PYTHON_3_11,
      code: Code.fromAsset('../src'),  // srcディレクトリを指定
      handler: 'main.lambda_handler',
      vpc: vpc,
      environment: {
        DB_HOST: 'localhost',
        DB_USER: 'admin',
        DB_PASSWORD: 'password',
        DB_NAME: props.dbName,
      }
    });

    // LambdaにSecrets Managerのアクセス権限を追加
    secret.grantRead(lambdaFunction);
  }
}
