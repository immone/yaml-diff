import streamlit as st
import yaml
from deepdiff import DeepDiff
import json

st.set_page_config(page_title="YAML Diff", layout="centered")

# Two columns for input
col1, col2 = st.columns(2)

with col1:
    st.subheader("YAML 1")
    yaml1_text = st.text_area(
        "First YAML",
        height=300,
        placeholder="Paste your first YAML here...",
        label_visibility="collapsed"
    )

with col2:
    st.subheader("YAML 2")
    yaml2_text = st.text_area(
        "Second YAML",
        height=300,
        placeholder="Paste your second YAML here...",
        label_visibility="collapsed"
    )

# Compare button
if st.button("Compare", type="primary", use_container_width=True):
    if not yaml1_text or not yaml2_text:
        st.warning("Please provide both YAML inputs")
    else:
        try:
            # Parse YAML
            data1 = yaml.safe_load(yaml1_text)
            data2 = yaml.safe_load(yaml2_text)
            
            # Find differences
            diff = DeepDiff(data1, data2, ignore_order=False, verbose_level=2)
            
            if not diff:
                st.success("✓ No differences found - YAMLs are identical")
            else:
                st.subheader("Differences Found")
                
                # Display each type of difference
                if 'values_changed' in diff:
                    st.markdown("**Changed Values:**")
                    for path, change in diff['values_changed'].items():
                        st.markdown(f"- `{path}`")
                        col_a, col_b = st.columns(2)
                        with col_a:
                            st.code(f"Old: {change['old_value']}", language=None)
                        with col_b:
                            st.code(f"New: {change['new_value']}", language=None)
                
                if 'dictionary_item_added' in diff:
                    st.markdown("**Added Items:**")
                    for item in diff['dictionary_item_added']:
                        st.markdown(f"- `{item}`")
                
                if 'dictionary_item_removed' in diff:
                    st.markdown("**Removed Items:**")
                    for item in diff['dictionary_item_removed']:
                        st.markdown(f"- `{item}`")
                
                if 'iterable_item_added' in diff:
                    st.markdown("**Added List Items:**")
                    for path, value in diff['iterable_item_added'].items():
                        st.markdown(f"- `{path}`: {value}")
                
                if 'iterable_item_removed' in diff:
                    st.markdown("**Removed List Items:**")
                    for path, value in diff['iterable_item_removed'].items():
                        st.markdown(f"- `{path}`: {value}")
                
                if 'type_changes' in diff:
                    st.markdown("**Type Changes:**")
                    for path, change in diff['type_changes'].items():
                        st.markdown(f"- `{path}`: {change['old_type'].__name__} → {change['new_type'].__name__}")
                
        except yaml.YAMLError as e:
            st.error(f"YAML parsing error: {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}")

# Sample data button
with st.expander("Load Sample Data"):
    if st.button("Load Example"):
        st.rerun()