#!/usr/bin/env bash
# ═══════════════════════════════════════════════════════════════
# CyberHoroscope — Frontend Deploy Script
# ═══════════════════════════════════════════════════════════════
# Usage:
#   chmod +x scripts/deploy_frontend.sh
#   ./scripts/deploy_frontend.sh
#
# Prerequisites:
#   - AWS CLI configured with deploy permissions
#   - SAM stack already deployed (sam deploy)
#   - jq installed (brew install jq  OR  apt install jq)
# ═══════════════════════════════════════════════════════════════

set -e

STACK_NAME="cyber-horoscope"
REGION="ap-south-1"
FRONTEND_SRC="frontend/index.html"
FRONTEND_TMP="/tmp/index.html"

echo ""
echo "🔮 CyberHoroscope — Frontend Deploy"
echo "════════════════════════════════════"

# ── Step 1: Read stack outputs ────────────────────────────────
echo ""
echo "📡 Fetching stack outputs from CloudFormation..."

STACK_OUTPUTS=$(aws cloudformation describe-stacks \
  --stack-name "$STACK_NAME" \
  --region "$REGION" \
  --query "Stacks[0].Outputs" \
  --output json)

API_ENDPOINT=$(echo "$STACK_OUTPUTS" | jq -r '.[] | select(.OutputKey=="ApiEndpoint") | .OutputValue')
BUCKET_NAME=$(echo  "$STACK_OUTPUTS" | jq -r '.[] | select(.OutputKey=="BucketName")  | .OutputValue')
CF_URL=$(echo       "$STACK_OUTPUTS" | jq -r '.[] | select(.OutputKey=="FrontendURL") | .OutputValue')

if [[ -z "$API_ENDPOINT" || "$API_ENDPOINT" == "null" ]]; then
  echo "❌ Could not read ApiEndpoint from stack outputs. Has 'sam deploy' been run?"
  exit 1
fi

echo "   ✅ API Endpoint : $API_ENDPOINT"
echo "   ✅ S3 Bucket    : $BUCKET_NAME"
echo "   ✅ CloudFront   : $CF_URL"

# ── Step 2: Get CloudFront distribution ID ────────────────────
echo ""
echo "🔍 Resolving CloudFront distribution ID..."

CF_DIST_ID=$(aws cloudfront list-distributions \
  --query "DistributionList.Items[?DomainName=='$(echo $CF_URL | sed "s|https://||")'].Id" \
  --output text)

if [[ -z "$CF_DIST_ID" ]]; then
  # Fallback: derive from stack resources
  CF_DIST_ID=$(aws cloudformation describe-stack-resources \
    --stack-name "$STACK_NAME" \
    --region "$REGION" \
    --query "StackResources[?ResourceType=='AWS::CloudFront::Distribution'].PhysicalResourceId" \
    --output text)
fi

echo "   ✅ Distribution ID : $CF_DIST_ID"

# ── Step 3: Inject API endpoint into frontend ─────────────────
echo ""
echo "🔧 Replacing __API_ENDPOINT__ placeholder in index.html..."

cp "$FRONTEND_SRC" "$FRONTEND_TMP"
sed -i "s|__API_ENDPOINT__|$API_ENDPOINT|g" "$FRONTEND_TMP"

# Verify replacement was made
if grep -q "__API_ENDPOINT__" "$FRONTEND_TMP"; then
  echo "❌ Replacement failed — __API_ENDPOINT__ still present. Check frontend/index.html."
  exit 1
fi
echo "   ✅ Placeholder replaced successfully"

# ── Step 4: Upload to S3 ──────────────────────────────────────
echo ""
echo "☁️  Uploading to S3 bucket: $BUCKET_NAME..."

aws s3 cp "$FRONTEND_TMP" "s3://$BUCKET_NAME/index.html" \
  --content-type "text/html" \
  --cache-control "max-age=300" \
  --region "$REGION"

echo "   ✅ Upload complete"

# ── Step 5: CloudFront cache invalidation ────────────────────
echo ""
echo "🔄 Invalidating CloudFront cache (distribution: $CF_DIST_ID)..."

INVALIDATION_ID=$(aws cloudfront create-invalidation \
  --distribution-id "$CF_DIST_ID" \
  --paths "/*" \
  --query "Invalidation.Id" \
  --output text)

echo "   ✅ Invalidation created: $INVALIDATION_ID"
echo "   ⏳ Cache may take 30–60 seconds to propagate globally"

# ── Step 6: Print live URL ────────────────────────────────────
echo ""
echo "════════════════════════════════════"
echo "🎉 Deploy complete!"
echo ""
echo "🌐 Live URL : $CF_URL"
echo "🔌 API URL  : $API_ENDPOINT"
echo ""
echo "Demo tip: open the URL, select all worst answers, click Reveal 🔮"
echo "════════════════════════════════════"
