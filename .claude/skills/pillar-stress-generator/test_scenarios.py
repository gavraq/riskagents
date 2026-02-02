"""
Test Suite for Pillar Stress Scenario Generator

Tests the complete workflow with three sample scenarios:
1. US Recession with Fed Policy Error
2. Middle East Oil Supply Disruption
3. EUR Sovereign Crisis 2.0
"""

import json
from pathlib import Path
from datetime import datetime

from scenario_designer import ScenarioDesigner, ScenarioType, Severity
from scenario_reviewer import ScenarioReviewer
from validators import ScenarioValidator
from parameterization_engine import ParameterizationEngine

class TestRunner:
    """Run comprehensive tests on the pillar stress generator."""

    def __init__(self):
        self.data_dir = Path(__file__).parent / "data"
        self.output_dir = Path(__file__).parent / "test_output"
        self.output_dir.mkdir(exist_ok=True)

        self.designer = ScenarioDesigner(self.data_dir)
        self.reviewer = ScenarioReviewer(self.data_dir)
        self.validator = ScenarioValidator()
        self.param_engine = ParameterizationEngine(self.data_dir)

    def run_all_tests(self):
        """Run all test scenarios."""
        print("=" * 80)
        print("PILLAR STRESS SCENARIO GENERATOR - TEST SUITE")
        print("=" * 80)
        print()

        # Test 1: US Recession with Fed Policy Error
        print("TEST 1: Creating US Recession with Fed Policy Error scenario...")
        test1_result = self.test_us_recession_policy_error()
        print(f"✅ Test 1 Complete - Confidence Score: {test1_result['confidence']:.0f}%")
        print()

        # Test 2: Middle East Oil Supply Disruption
        print("TEST 2: Creating Middle East Oil Supply Disruption scenario...")
        test2_result = self.test_oil_supply_disruption()
        print(f"✅ Test 2 Complete - Confidence Score: {test2_result['confidence']:.0f}%")
        print()

        # Test 3: EUR Sovereign Crisis 2.0
        print("TEST 3: Creating EUR Sovereign Crisis 2.0 scenario...")
        test3_result = self.test_eur_sovereign_crisis()
        print(f"✅ Test 3 Complete - Confidence Score: {test3_result['confidence']:.0f}%")
        print()

        # Test 4: Annual Review
        print("TEST 4: Conducting annual review of existing scenario...")
        test4_result = self.test_annual_review()
        print(f"✅ Test 4 Complete - Recommendation: {test4_result['recommendation']}")
        print()

        # Summary
        self.print_test_summary([test1_result, test2_result, test3_result, test4_result])

        return {
            "test1": test1_result,
            "test2": test2_result,
            "test3": test3_result,
            "test4": test4_result
        }

    def test_us_recession_policy_error(self):
        """Test 1: US Recession with Fed Policy Error."""
        scenario = self.designer.create_scenario(
            scenario_name="US Recession with Fed Policy Error",
            trigger_event="Federal Reserve overtightens monetary policy despite weakening economy, triggering hard landing",
            scenario_type=ScenarioType.POLICY_ERROR,
            severity=Severity.SEVERE,
            primary_geography="US",
            narrative_elements=["policy_error", "recession"],
            transmission_channels=[
                "Fed raises rates 50bps despite negative GDP print and labor market weakness",
                "Corporate credit spreads widen sharply as refinancing becomes problematic",
                "USD strengthens on rate differentials despite US recession",
                "EM currencies depreciate on capital flight",
                "Equity markets decline on earnings downgrades and higher discount rates"
            ],
            key_assumptions=[
                "Fed prioritizes inflation target over growth",
                "Long and variable lags in monetary policy transmission",
                "Corporate sector overleveraged after years of low rates",
                "Labor market softens but inflation remains sticky at 3.5%"
            ],
            timeline={
                "onset": "Q1 2025 - Fed hikes despite weak data",
                "peak": "Q2-Q3 2025 - Recession materializes, credit stress emerges",
                "recovery": "Q4 2025-Q1 2026 - Fed pivots, gradual stabilization"
            }
        )

        # Save scenario
        output_file = self.designer.save_scenario(scenario, self.output_dir / "test1")

        # Generate validation report
        validation_report = self.validator.generate_validation_report(scenario.validation_results)

        # Save validation report
        with open(self.output_dir / "test1" / "validation_report.md", 'w') as f:
            f.write(validation_report)

        print(f"   📄 Scenario saved to: {output_file}")
        print(f"   📊 Asset classes: {len(scenario.asset_class_shocks)}")
        print(f"   ✅ Validation: {len([v for v in scenario.validation_results if v.level.value == 'error'])} errors, {len([v for v in scenario.validation_results if v.level.value == 'warning'])} warnings")
        print(f"   🎯 Confidence: {scenario.confidence_score:.0f}%")

        return {
            "name": scenario.metadata.scenario_name,
            "confidence": scenario.confidence_score,
            "validation_errors": len([v for v in scenario.validation_results if v.level.value == 'error']),
            "validation_warnings": len([v for v in scenario.validation_results if v.level.value == 'warning']),
            "asset_classes": len(scenario.asset_class_shocks),
            "output_file": str(output_file)
        }

    def test_oil_supply_disruption(self):
        """Test 2: Middle East Oil Supply Disruption."""
        scenario = self.designer.create_scenario(
            scenario_name="Middle East Oil Supply Disruption",
            trigger_event="Regional conflict escalates, disrupting 3 million barrels/day of oil exports through critical shipping lanes",
            scenario_type=ScenarioType.SUPPLY_DISRUPTION,
            severity=Severity.SEVERE,
            primary_geography="global",
            narrative_elements=["oil_supply_shock", "inflation_expectations"],
            transmission_channels=[
                "Oil prices spike 50% as supply is physically disrupted",
                "Inflation expectations rise sharply, forcing central bank tightening",
                "Energy-importing economies see terms of trade deterioration",
                "Gas prices follow oil higher on energy complex correlation",
                "Consumer spending constrained by higher energy costs, growth slows"
            ],
            key_assumptions=[
                "Disruption lasts 6+ months (not quickly resolved)",
                "Strategic petroleum reserves provide limited buffer",
                "OPEC+ unable or unwilling to fully offset supply loss",
                "Limited demand destruction despite high prices"
            ],
            timeline={
                "onset": "Immediate - conflict escalation, shipping halt",
                "peak": "1-2 months - oil peaks at $135/bbl, policy response begins",
                "recovery": "6-12 months - diplomatic resolution, supply gradually restored"
            }
        )

        output_file = self.designer.save_scenario(scenario, self.output_dir / "test2")
        validation_report = self.validator.generate_validation_report(scenario.validation_results)

        with open(self.output_dir / "test2" / "validation_report.md", 'w') as f:
            f.write(validation_report)

        print(f"   📄 Scenario saved to: {output_file}")
        print(f"   📊 Asset classes: {len(scenario.asset_class_shocks)}")
        print(f"   ✅ Validation: {len([v for v in scenario.validation_results if v.level.value == 'error'])} errors, {len([v for v in scenario.validation_results if v.level.value == 'warning'])} warnings")
        print(f"   🎯 Confidence: {scenario.confidence_score:.0f}%")

        return {
            "name": scenario.metadata.scenario_name,
            "confidence": scenario.confidence_score,
            "validation_errors": len([v for v in scenario.validation_results if v.level.value == 'error']),
            "validation_warnings": len([v for v in scenario.validation_results if v.level.value == 'warning']),
            "asset_classes": len(scenario.asset_class_shocks),
            "output_file": str(output_file)
        }

    def test_eur_sovereign_crisis(self):
        """Test 3: EUR Sovereign Crisis 2.0."""
        scenario = self.designer.create_scenario(
            scenario_name="EUR Sovereign Crisis 2.0",
            trigger_event="Sovereign debt crisis re-emerges in peripheral EUR economies amid fiscal deterioration and political fragmentation",
            scenario_type=ScenarioType.RECESSION,
            severity=Severity.SEVERE,
            primary_geography="EUR",
            narrative_elements=["sovereign_stress", "banking_stress"],
            transmission_channels=[
                "Peripheral sovereign spreads widen sharply (Italy, Spain, Portugal)",
                "Sovereign-bank doom loop re-emerges as banks hold government debt",
                "EUR depreciates on capital flight and ECB credibility concerns",
                "Credit spreads widen, especially for EUR financials",
                "Flight to quality into German Bunds and USD"
            ],
            key_assumptions=[
                "ECB constrained by inflation, cannot immediately ease",
                "Fiscal rules prevent aggressive national responses",
                "Political will for bailouts limited vs 2011-2012",
                "Contagion contained to EUR (limited global spillover)"
            ],
            timeline={
                "onset": "Q2 2025 - Sovereign debt auction fails, spreads spike",
                "peak": "Q3 2025 - Banking sector stress, EUR weakness accelerates",
                "recovery": "Q4 2025-Q1 2026 - ECB intervention, fiscal support package"
            }
        )

        output_file = self.designer.save_scenario(scenario, self.output_dir / "test3")
        validation_report = self.validator.generate_validation_report(scenario.validation_results)

        with open(self.output_dir / "test3" / "validation_report.md", 'w') as f:
            f.write(validation_report)

        print(f"   📄 Scenario saved to: {output_file}")
        print(f"   📊 Asset classes: {len(scenario.asset_class_shocks)}")
        print(f"   ✅ Validation: {len([v for v in scenario.validation_results if v.level.value == 'error'])} errors, {len([v for v in scenario.validation_results if v.level.value == 'warning'])} warnings")
        print(f"   🎯 Confidence: {scenario.confidence_score:.0f}%")

        return {
            "name": scenario.metadata.scenario_name,
            "confidence": scenario.confidence_score,
            "validation_errors": len([v for v in scenario.validation_results if v.level.value == 'error']),
            "validation_warnings": len([v for v in scenario.validation_results if v.level.value == 'warning']),
            "asset_classes": len(scenario.asset_class_shocks),
            "output_file": str(output_file)
        }

    def test_annual_review(self):
        """Test 4: Annual Review of Existing Scenario."""
        review_result = self.reviewer.review_scenario(
            scenario_name="Financial Crisis 2025",
            reviewer="Market Risk",
            market_changes=[
                "Volatility regime has shifted higher vs 2024",
                "EM spreads have compressed significantly"
            ],
            system_changes=[
                "Base Metals migrating to Murex (in progress, target 2025)",
                "Precious Metals vol shocks changed to relative (Murex)"
            ],
            trading_changes={
                "Base Metals": [
                    "Iron Ore trading discontinued",
                    "Cobalt trading added"
                ]
            }
        )

        # Generate review memo
        memo = self.reviewer.generate_review_memo(review_result)

        # Save memo
        output_file = self.output_dir / "test4" / "annual_review_memo.md"
        output_file.parent.mkdir(exist_ok=True)
        with open(output_file, 'w') as f:
            f.write(memo)

        print(f"   📄 Review memo saved to: {output_file}")
        print(f"   📊 Asset classes reviewed: {len(review_result.asset_class_reviews)}")

        changes = [r for r in review_result.asset_class_reviews if r.change_type.value != 'no_change']
        print(f"   🔄 Changes proposed: {len(changes)}")
        print(f"   ✅ Recommendation: {review_result.recommended_action}")

        return {
            "scenario": review_result.scenario_name,
            "recommendation": review_result.recommended_action,
            "changes_proposed": len(changes),
            "output_file": str(output_file)
        }

    def print_test_summary(self, results):
        """Print summary of all tests."""
        print("=" * 80)
        print("TEST SUMMARY")
        print("=" * 80)
        print()

        print("📊 Scenario Creation Tests:")
        for i, result in enumerate(results[:3], 1):
            print(f"   Test {i}: {result['name']}")
            print(f"      Confidence: {result['confidence']:.0f}%")
            print(f"      Validation: {result['validation_errors']} errors, {result['validation_warnings']} warnings")
            print(f"      Asset Classes: {result['asset_classes']}")
            print()

        print("📋 Annual Review Test:")
        result = results[3]
        print(f"   Scenario: {result['scenario']}")
        print(f"   Recommendation: {result['recommendation']}")
        print(f"   Changes: {result['changes_proposed']}")
        print()

        # Overall Assessment
        all_passed = all(r['validation_errors'] == 0 for r in results[:3])
        print("=" * 80)
        if all_passed:
            print("✅ ALL TESTS PASSED - No validation errors detected")
        else:
            print("⚠️  Some validation warnings present - review recommended")
        print("=" * 80)
        print()

        print(f"📁 All test outputs saved to: {self.output_dir}")
        print()


def main():
    """Run the test suite."""
    runner = TestRunner()
    results = runner.run_all_tests()

    # Save summary
    summary_file = runner.output_dir / "test_summary.json"
    with open(summary_file, 'w') as f:
        json.dump(results, f, indent=2)

    print(f"📊 Test summary saved to: {summary_file}")
    print()
    print("🎉 Testing complete!")

if __name__ == "__main__":
    main()
