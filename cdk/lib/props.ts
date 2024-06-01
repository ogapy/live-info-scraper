import { StackProps } from 'aws-cdk-lib';

export interface LiveInfoScraperProps extends StackProps {
    dbName: string;  // カスタムプロパティを追加
}
